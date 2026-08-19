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
                