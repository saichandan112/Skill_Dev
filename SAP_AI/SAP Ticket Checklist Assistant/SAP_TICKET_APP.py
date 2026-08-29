"""
SAP Ticket Checklist Assistant
Single-file Windows desktop application.

Features:
- Enter/resume a ticket number
- Select a ticket type
- Manually tick checklist steps in mandatory sequence
- Optional screenshot evidence per step
- Persistent SQLite storage
- Audit trail
- Export a Word-compatible HTML report

Run:
    python sap_ticket_assistant.py

No external packages are required.
"""

import html
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "SAP Ticket Checklist Assistant"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "TicketData"
DB_PATH = DATA_DIR / "ticket_assistant.db"

# Set to True if every step must have a sanitized PNG/JPG image before it can be ticked.
REQUIRE_EVIDENCE = False

CHECKLISTS = {
    "RegWeb": [
        ("Confirm incident details", "Review the ticket description, timestamps, impact, and sanitized error details."),
        ("Validate service availability", "Check the approved monitoring tools and service health indicators."),
        ("Review relevant logs", "Review approved logs without copying production-sensitive information."),
        ("Apply approved resolution", "Follow the current support runbook and required change approvals."),
        ("Validate service restoration", "Confirm expected behavior using an approved validation procedure."),
        ("Update ticket", "Document actions, results, and evidence before closure."),
    ],
    "W4 Forms": [
        ("Confirm request details", "Validate the issue description and affected process using sanitized information."),
        ("Review form configuration", "Check approved configuration and relevant form settings."),
        ("Review processing logs", "Inspect approved logs and identify the failure point."),
        ("Apply approved correction", "Use the authorized support procedure and required approvals."),
        ("Validate form processing", "Confirm successful processing using a sanitized test scenario."),
        ("Update ticket", "Document the outcome and attach approved evidence."),
    ],
    "Job Failure": [
        ("Verify job status", "Review the job status and execution timestamps in the approved monitoring tool."),
        ("Check job logs", "Review job log, runtime errors, spool status, and the previous successful run."),
        ("Verify dependencies", "Check predecessor jobs, files, interfaces, variants, and required resources."),
        ("Restart using approved procedure", "Restart only when the runbook and required approvals permit it."),
        ("Validate execution", "Confirm successful completion and validate downstream dependencies."),
        ("Update ticket", "Record the cause, action, result, timestamps, and sanitized evidence."),
    ],
    "YTD": [
        ("Confirm issue scope", "Validate the reported YTD issue and affected process without storing business values."),
        ("Review configuration", "Check approved payroll/YTD configuration and recent authorized changes."),
        ("Review processing status", "Review approved logs and status indicators using sanitized evidence."),
        ("Apply approved procedure", "Follow the current runbook and change-control requirements."),
        ("Validate correction", "Confirm the expected result using an approved validation method."),
        ("Update ticket", "Document actions and attach sanitized evidence."),
    ],
    "Payroll": [
        ("Confirm issue scope", "Confirm the payroll process, timing, and impact without recording payroll values."),
        ("Review process status", "Check approved status screens and technical logs."),
        ("Review dependencies", "Check jobs, interfaces, configuration, and authorized recent changes."),
        ("Apply approved procedure", "Use only the authorized support runbook and required approvals."),
        ("Validate processing", "Confirm the technical result without storing employee or payroll information."),
        ("Update ticket", "Record sanitized technical details and evidence."),
    ],
    "Interface Failure": [
        ("Confirm interface status", "Review monitoring status, timestamps, and sanitized error information."),
        ("Review technical logs", "Check approved interface and middleware logs without storing payload data."),
        ("Verify dependencies", "Check endpoints, certificates, jobs, queues, and connectivity through approved tools."),
        ("Reprocess using approved procedure", "Reprocess only under the current runbook and required approvals."),
        ("Validate end-to-end completion", "Confirm successful technical completion and downstream receipt."),
        ("Update ticket", "Document the result without including interface payloads or confidential data."),
    ],
    "Transport Issue": [
        ("Confirm transport details", "Review transport identifier, route, status, and approved change record."),
        ("Review import logs", "Inspect approved import logs and sanitized error details."),
        ("Verify dependencies", "Check sequence, prerequisites, locks, and environment readiness."),
        ("Apply approved correction", "Follow transport governance and obtain required approvals."),
        ("Validate import", "Confirm import completion and perform approved technical checks."),
        ("Update ticket", "Document actions, approvals, outcome, and sanitized evidence."),
    ],
    "Others": [
        ("Confirm incident details", "Review ticket description, impact, timestamps, and sanitized error details."),
        ("Identify approved runbook", "Locate the relevant support procedure and confirm ownership."),
        ("Perform technical investigation", "Use approved tools and avoid storing production business data."),
        ("Apply approved resolution", "Proceed only with the required authorization and change controls."),
        ("Validate resolution", "Confirm the expected technical outcome."),
        ("Update ticket", "Document the resolution and sanitized evidence."),
    ],
}


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def normalize_ticket_id(value):
    value = re.sub(r"\s+", "", value.strip().upper())
    if not re.fullmatch(r"[A-Z0-9_-]{4,30}", value):
        raise ValueError("Use 4-30 letters, numbers, underscores, or hyphens.")
    return value


def safe_ticket_folder(ticket_id):
    folder = DATA_DIR / ticket_id
    (folder / "screenshots").mkdir(parents=True, exist_ok=True)
    (folder / "report").mkdir(parents=True, exist_ok=True)
    return folder


class Database:
    def __init__(self, path):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                ticket_type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'IN_PROGRESS',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS steps (
                ticket_id TEXT NOT NULL,
                step_no INTEGER NOT NULL,
                step_name TEXT NOT NULL,
                guidance TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                completed_at TEXT,
                evidence_path TEXT,
                PRIMARY KEY (ticket_id, step_no),
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                details TEXT NOT NULL,
                event_at TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def get_ticket(self, ticket_id):
        return self.conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()

    def create_ticket(self, ticket_id, ticket_type):
        ts = now()
        with self.conn:
            self.conn.execute(
                "INSERT INTO tickets VALUES (?, ?, 'IN_PROGRESS', ?, ?)",
                (ticket_id, ticket_type, ts, ts),
            )
            for number, (name, guidance) in enumerate(CHECKLISTS[ticket_type], 1):
                self.conn.execute(
                    "INSERT INTO steps(ticket_id, step_no, step_name, guidance) VALUES (?, ?, ?, ?)",
                    (ticket_id, number, name, guidance),
                )
            self.audit(ticket_id, "TICKET_CREATED", f"Ticket created as {ticket_type}", commit=False)

    def steps(self, ticket_id):
        return self.conn.execute(
            "SELECT * FROM steps WHERE ticket_id=? ORDER BY step_no", (ticket_id,)
        ).fetchall()

    def set_evidence(self, ticket_id, step_no, path):
        with self.conn:
            self.conn.execute(
                "UPDATE steps SET evidence_path=? WHERE ticket_id=? AND step_no=?",
                (str(path), ticket_id, step_no),
            )
            self.audit(ticket_id, "EVIDENCE_ATTACHED", f"Step {step_no}: {Path(path).name}", commit=False)

    def complete_step(self, ticket_id, step_no):
        steps = self.steps(ticket_id)
        target = next(row for row in steps if row["step_no"] == step_no)
        if target["completed"]:
            return
        pending_before = [row for row in steps if row["step_no"] < step_no and not row["completed"]]
        if pending_before:
            raise ValueError(f"Complete Step {pending_before[0]['step_no']} first.")
        if REQUIRE_EVIDENCE and not target["evidence_path"]:
            raise ValueError("Attach sanitized screenshot evidence before completing this step.")
        ts = now()
        with self.conn:
            self.conn.execute(
                "UPDATE steps SET completed=1, completed_at=? WHERE ticket_id=? AND step_no=?",
                (ts, ticket_id, step_no),
            )
            self.conn.execute(
                "UPDATE tickets SET updated_at=? WHERE ticket_id=?", (ts, ticket_id)
            )
            self.audit(ticket_id, "STEP_COMPLETED", f"Step {step_no}: {target['step_name']}", commit=False)

    def reopen_step(self, ticket_id, step_no):
        steps = self.steps(ticket_id)
        later_done = [row for row in steps if row["step_no"] > step_no and row["completed"]]
        if later_done:
            raise ValueError("Reopen later completed steps first to preserve checklist order.")
        with self.conn:
            self.conn.execute(
                "UPDATE steps SET completed=0, completed_at=NULL WHERE ticket_id=? AND step_no=?",
                (ticket_id, step_no),
            )
            self.conn.execute(
                "UPDATE tickets SET status='IN_PROGRESS', updated_at=? WHERE ticket_id=?",
                (now(), ticket_id),
            )
            self.audit(ticket_id, "STEP_REOPENED", f"Step {step_no} reopened", commit=False)

    def close_ticket(self, ticket_id):
        pending = [row for row in self.steps(ticket_id) if not row["completed"]]
        if pending:
            raise ValueError(f"Cannot close. Step {pending[0]['step_no']} is still pending.")
        with self.conn:
            self.conn.execute(
                "UPDATE tickets SET status='COMPLETED', updated_at=? WHERE ticket_id=?",
                (now(), ticket_id),
            )
            self.audit(ticket_id, "TICKET_COMPLETED", "All mandatory steps completed", commit=False)

    def audit(self, ticket_id, event_type, details, commit=True):
        self.conn.execute(
            "INSERT INTO audit_events(ticket_id,event_type,details,event_at) VALUES(?,?,?,?)",
            (ticket_id, event_type, details, now()),
        )
        if commit:
            self.conn.commit()

    def audit_events(self, ticket_id):
        return self.conn.execute(
            "SELECT * FROM audit_events WHERE ticket_id=? ORDER BY event_id", (ticket_id,)
        ).fetchall()


class TicketAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1000x700")
        self.minsize(850, 600)
        self.db = Database(DB_PATH)
        self.ticket_id = None
        self.vars = {}
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")

        header = ttk.Frame(self, padding=14)
        header.pack(fill="x")
        ttk.Label(header, text=APP_TITLE, font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=6, sticky="w")
        ttk.Label(header, text="Guided manual checklist. Approved SAP runbooks and change controls remain mandatory.").grid(row=1, column=0, columnspan=6, sticky="w", pady=(2, 12))

        ttk.Label(header, text="Ticket number:").grid(row=2, column=0, sticky="w")
        self.ticket_entry = ttk.Entry(header, width=24)
        self.ticket_entry.grid(row=2, column=1, padx=(6, 18), sticky="w")
        ttk.Label(header, text="Ticket type:").grid(row=2, column=2, sticky="w")
        self.type_combo = ttk.Combobox(header, values=list(CHECKLISTS), state="readonly", width=22)
        self.type_combo.set("Job Failure")
        self.type_combo.grid(row=2, column=3, padx=(6, 18), sticky="w")
        ttk.Button(header, text="Create / Resume", command=self.load_ticket).grid(row=2, column=4, padx=4)
        ttk.Button(header, text="New Screen", command=self.reset_screen).grid(row=2, column=5, padx=4)

        self.summary = ttk.Label(self, text="Enter a ticket number to begin.", padding=(14, 6), font=("Segoe UI", 10, "bold"))
        self.summary.pack(fill="x")

        container = ttk.Frame(self, padding=(14, 4, 14, 8))
        container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.steps_frame = ttk.Frame(self.canvas)
        self.steps_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.steps_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"))

        footer = ttk.Frame(self, padding=14)
        footer.pack(fill="x")
        ttk.Button(footer, text="Validate and Close Ticket", command=self.close_ticket).pack(side="left")
        ttk.Button(footer, text="Export Evidence Report", command=self.export_report).pack(side="left", padx=8)
        ttk.Button(footer, text="Open Ticket Folder", command=self.open_ticket_folder).pack(side="left")
        self.status = ttk.Label(footer, text="Ready", anchor="e")
        self.status.pack(side="right", fill="x", expand=True)

    def load_ticket(self):
        try:
            ticket_id = normalize_ticket_id(self.ticket_entry.get())
        except ValueError as exc:
            messagebox.showerror("Invalid ticket number", str(exc))
            return
        ticket = self.db.get_ticket(ticket_id)
        if ticket is None:
            ticket_type = self.type_combo.get()
            if not ticket_type:
                messagebox.showerror("Ticket type required", "Select a ticket type.")
                return
            self.db.create_ticket(ticket_id, ticket_type)
            safe_ticket_folder(ticket_id)
            ticket = self.db.get_ticket(ticket_id)
        self.ticket_id = ticket_id
        self.type_combo.set(ticket["ticket_type"])
        self.type_combo.configure(state="disabled")
        self.render_steps()
        self.status.configure(text=f"Loaded {ticket_id}")

    def render_steps(self):
        for widget in self.steps_frame.winfo_children():
            widget.destroy()
        self.vars.clear()
        if not self.ticket_id:
            return
        ticket = self.db.get_ticket(self.ticket_id)
        steps = self.db.steps(self.ticket_id)
        completed_count = sum(row["completed"] for row in steps)
        self.summary.configure(
            text=f"Ticket: {self.ticket_id}   |   Type: {ticket['ticket_type']}   |   Status: {ticket['status']}   |   Progress: {completed_count}/{len(steps)}"
        )

        first_pending = next((row["step_no"] for row in steps if not row["completed"]), None)
        for row in steps:
            card = ttk.LabelFrame(self.steps_frame, text=f"Step {row['step_no']}: {row['step_name']}", padding=10)
            card.pack(fill="x", expand=True, pady=5, padx=2)
            ttk.Label(card, text=row["guidance"], wraplength=790, justify="left").grid(row=0, column=0, columnspan=3, sticky="w")
            evidence_name = Path(row["evidence_path"]).name if row["evidence_path"] else "No evidence attached"
            evidence_label = ttk.Label(card, text=f"Evidence: {evidence_name}")
            evidence_label.grid(row=1, column=0, sticky="w", pady=(8, 4))
            ttk.Button(card, text="Attach Sanitized Screenshot", command=lambda n=row["step_no"]: self.attach_evidence(n)).grid(row=1, column=1, padx=8)

            var = tk.BooleanVar(value=bool(row["completed"]))
            self.vars[row["step_no"]] = var
            state = "normal" if row["completed"] or row["step_no"] == first_pending else "disabled"
            checkbox = ttk.Checkbutton(
                card,
                text="Completed manually",
                variable=var,
                state=state,
                command=lambda n=row["step_no"], v=var: self.toggle_step(n, v),
            )
            checkbox.grid(row=1, column=2, padx=8, sticky="e")
            if row["completed_at"]:
                ttk.Label(card, text=f"Completed: {row['completed_at']}", foreground="green").grid(row=2, column=0, columnspan=3, sticky="w")
            card.columnconfigure(0, weight=1)

    def toggle_step(self, step_no, variable):
        try:
            if variable.get():
                self.db.complete_step(self.ticket_id, step_no)
            else:
                self.db.reopen_step(self.ticket_id, step_no)
            self.render_steps()
        except ValueError as exc:
            variable.set(not variable.get())
            messagebox.showwarning("Checklist validation", str(exc))

    def attach_evidence(self, step_no):
        if not self.ticket_id:
            return
        approved = messagebox.askyesno(
            "Sanitized evidence confirmation",
            "Confirm that the selected image is sanitized, approved for ticket documentation, and contains no credentials, payroll values, employee data, or confidential business information.",
        )
        if not approved:
            return
        source = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")])
        if not source:
            return
        source_path = Path(source)
        if source_path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            messagebox.showerror("Invalid evidence", "Select a PNG or JPEG image.")
            return
        destination = safe_ticket_folder(self.ticket_id) / "screenshots" / f"step_{step_no:02d}{source_path.suffix.lower()}"
        try:
            shutil.copy2(source_path, destination)
            self.db.set_evidence(self.ticket_id, step_no, destination)
            self.render_steps()
        except OSError as exc:
            messagebox.showerror("Evidence error", str(exc))

    def close_ticket(self):
        if not self.ticket_id:
            messagebox.showinfo("No ticket", "Create or resume a ticket first.")
            return
        try:
            self.db.close_ticket(self.ticket_id)
            self.render_steps()
            messagebox.showinfo("Ticket checklist complete", "All mandatory checklist steps are complete. The ticket is ready for the approved closure process.")
        except ValueError as exc:
            messagebox.showwarning("Closure blocked", str(exc))

    def export_report(self):
        if not self.ticket_id:
            messagebox.showinfo("No ticket", "Create or resume a ticket first.")
            return
        ticket = self.db.get_ticket(self.ticket_id)
        steps = self.db.steps(self.ticket_id)
        if any(not row["completed"] for row in steps):
            messagebox.showwarning("Report blocked", "Complete every mandatory step before exporting the final report.")
            return
        events = self.db.audit_events(self.ticket_id)
        report_path = safe_ticket_folder(self.ticket_id) / "report" / f"{self.ticket_id}_analysis.html"
        step_sections = []
        for row in steps:
            evidence = row["evidence_path"] or "Not attached"
            step_sections.append(f"""
                <h2>Step {row['step_no']}: {html.escape(row['step_name'])}</h2>
                <p><b>Status:</b> Completed</p>
                <p><b>Completed:</b> {html.escape(row['completed_at'] or '')}</p>
                <p><b>Guidance:</b> {html.escape(row['guidance'])}</p>
                <p><b>Evidence:</b> {html.escape(str(evidence))}</p>
            """)
        audit_rows = "".join(
            f"<tr><td>{e['event_id']}</td><td>{html.escape(e['event_at'])}</td><td>{html.escape(e['event_type'])}</td><td>{html.escape(e['details'])}</td></tr>"
            for e in events
        )
        document = f"""<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(self.ticket_id)} Evidence Report</title>
        <style>body{{font-family:Segoe UI,Arial;margin:40px;color:#222}}h1{{color:#0f4c81}}h2{{border-bottom:1px solid #ccc;padding-bottom:5px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #aaa;padding:7px;text-align:left}}.notice{{background:#fff4ce;padding:12px;border-left:4px solid #ffb900}}</style></head><body>
        <h1>SAP Ticket Checklist Evidence Report</h1>
        <p><b>Ticket ID:</b> {html.escape(ticket['ticket_id'])}<br><b>Ticket type:</b> {html.escape(ticket['ticket_type'])}<br><b>Status:</b> {html.escape(ticket['status'])}<br><b>Created:</b> {html.escape(ticket['created_at'])}<br><b>Generated:</b> {html.escape(now())}</p>
        <div class='notice'><b>Privacy notice:</b> This report is intended to contain only sanitized technical evidence. Approved support procedures, access controls, retention rules, and change approvals remain mandatory.</div>
        {''.join(step_sections)}
        <h2>Audit Trail</h2><table><tr><th>ID</th><th>Timestamp</th><th>Event</th><th>Details</th></tr>{audit_rows}</table>
        </body></html>"""
        report_path.write_text(document, encoding="utf-8")
        self.db.audit(self.ticket_id, "REPORT_EXPORTED", report_path.name)
        messagebox.showinfo("Report exported", f"Report created:\n{report_path}\n\nThe HTML file can be opened in Microsoft Word and saved as DOCX.")
        self._open_path(report_path)

    def open_ticket_folder(self):
        if not self.ticket_id:
            messagebox.showinfo("No ticket", "Create or resume a ticket first.")
            return
        self._open_path(safe_ticket_folder(self.ticket_id))

    @staticmethod
    def _open_path(path):
        try:
            if os.name == "nt":
                os.startfile(str(path))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except OSError:
            pass

    def reset_screen(self):
        self.ticket_id = None
        self.ticket_entry.delete(0, "end")
        self.type_combo.configure(state="readonly")
        self.type_combo.set("Job Failure")
        for widget in self.steps_frame.winfo_children():
            widget.destroy()
        self.summary.configure(text="Enter a ticket number to begin.")
        self.status.configure(text="Ready")


if __name__ == "__main__":
    TicketAssistant().mainloop()
