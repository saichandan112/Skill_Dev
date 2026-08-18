"""Tkinter desktop user interface."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from modules.config import load_app_config, resolve_path
from modules.checklist import ChecklistRepository
from modules.database import Database
from modules.document_generator import DocumentGenerator
from modules.logger import TicketLogger
from modules.report_generator import ReportGenerator
from modules.screenshot_manager import ScreenshotManager
from modules.session_manager import SessionManager
from modules.validator import Validator, ValidationError


class TicketAssistantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config_data = load_app_config()
        self.title(f"{self.config_data['application_name']} v{self.config_data['version']}")
        self.geometry("980x720")
        self.minsize(850, 620)

        self.repo = ChecklistRepository()
        self.db = Database(resolve_path(self.config_data['database_path']))
        self.sessions = SessionManager(resolve_path(self.config_data['data_root']))
        self.validator = Validator(self.config_data['allowed_ticket_pattern'])
        self.ticket_logger = TicketLogger()
        self.doc_generator = DocumentGenerator(self.config_data.get('organization_name', ''))
        self.report_generator = ReportGenerator(self.db, self.doc_generator)

        self.ticket_id = None
        self.ticket_paths = None
        self.steps = []
        self.current_step = None
        self.evidence_path = None
        self._build()

    def _build(self):
        header = ttk.Frame(self, padding=12)
        header.pack(fill='x')
        ttk.Label(header, text="SAP AI Ticket Assistant", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=4, sticky='w')
        ttk.Label(header, text="Guided checklist, evidence control, audit logging, and Word reporting", foreground='#444').grid(row=1, column=0, columnspan=4, sticky='w', pady=(0, 12))
        ttk.Label(header, text="Ticket ID").grid(row=2, column=0, sticky='w')
        self.ticket_entry = ttk.Entry(header, width=24)
        self.ticket_entry.grid(row=3, column=0, sticky='ew', padx=(0, 8))
        ttk.Label(header, text="Ticket Type").grid(row=2, column=1, sticky='w')
        self.issue_combo = ttk.Combobox(header, values=self.repo.issue_types(), state='readonly', width=25)
        self.issue_combo.grid(row=3, column=1, sticky='ew', padx=(0, 8))
        self.issue_combo.set(self.repo.issue_types()[0])
        ttk.Button(header, text="Start New", command=self.start_new).grid(row=3, column=2, padx=4)
        ttk.Button(header, text="Resume", command=self.resume).grid(row=3, column=3, padx=4)
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)

        privacy = ttk.LabelFrame(self, text="Privacy and Evidence Control", padding=10)
        privacy.pack(fill='x', padx=12, pady=(0, 8))
        ttk.Label(privacy, text="Use sanitized technical screenshots only. Never capture employee, payroll, tax, payload, database, or other production business data.", foreground='#9a3412', wraplength=900).pack(anchor='w')
        self.sanitized_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(privacy, text="I confirm the evidence is sanitized and approved for ticket documentation.", variable=self.sanitized_var).pack(anchor='w', pady=(6, 0))

        body = ttk.Frame(self, padding=(12, 4, 12, 12))
        body.pack(fill='both', expand=True)
        left = ttk.LabelFrame(body, text="Mandatory Steps", padding=8)
        left.pack(side='left', fill='y', padx=(0, 8))
        self.step_list = tk.Listbox(left, width=38, height=25, exportselection=False)
        self.step_list.pack(fill='both', expand=True)
        self.step_list.bind('<<ListboxSelect>>', self.select_step)

        right = ttk.LabelFrame(body, text="Guided Troubleshooting", padding=12)
        right.pack(side='left', fill='both', expand=True)
        self.status_label = ttk.Label(right, text="Enter or resume a ticket to begin.", font=("Segoe UI", 12, "bold"), wraplength=550)
        self.status_label.pack(anchor='w')
        self.guidance = tk.Text(right, height=15, wrap='word', state='disabled', font=("Segoe UI", 10))
        self.guidance.pack(fill='both', expand=True, pady=10)
        self.evidence_label = ttk.Label(right, text="Evidence: Not selected", wraplength=550)
        self.evidence_label.pack(anchor='w', pady=(0, 8))

        actions = ttk.Frame(right)
        actions.pack(fill='x')
        ttk.Button(actions, text="Import Sanitized Screenshot", command=self.import_evidence).pack(side='left', padx=(0, 6))
        if self.config_data.get('allow_live_screenshot_capture', False):
            ttk.Button(actions, text="Capture Screen", command=self.capture_screen).pack(side='left', padx=(0, 6))
        ttk.Button(actions, text="Complete Current Step", command=self.complete_step).pack(side='left', padx=(0, 6))
        ttk.Button(actions, text="Finalize and Generate Word Report", command=self.finalize).pack(side='right')

    def start_new(self):
        try:
            ticket_id = self.validator.ticket_id(self.ticket_entry.get())
            if self.db.ticket_exists(ticket_id):
                raise ValidationError("This ticket already exists. Use Resume.")
            issue_type = self.issue_combo.get()
            paths = self.sessions.ticket_paths(ticket_id)
            self.db.create_ticket(ticket_id, issue_type, self.repo.get(issue_type))
            self.ticket_logger.for_ticket(ticket_id, paths['logs']).info("Ticket created: %s", issue_type)
            self.load_ticket(ticket_id)
        except Exception as exc:
            messagebox.showerror("Cannot start ticket", str(exc))

    def resume(self):
        try:
            ticket_id = self.validator.ticket_id(self.ticket_entry.get())
            if not self.db.ticket_exists(ticket_id):
                raise ValidationError("Ticket not found. Use Start New.")
            self.load_ticket(ticket_id)
        except Exception as exc:
            messagebox.showerror("Cannot resume ticket", str(exc))

    def load_ticket(self, ticket_id):
        self.ticket_id = ticket_id
        self.ticket_paths = self.sessions.ticket_paths(ticket_id)
        self.steps = self.db.get_steps(ticket_id)
        self.refresh_steps()
        pending = self.validator.next_pending(self.steps)
        if pending:
            self.step_list.selection_clear(0, 'end')
            self.step_list.selection_set(pending['step_number'] - 1)
            self.show_step(pending)
        else:
            self.status_label.config(text=f"{ticket_id}: All steps complete. Generate the final report.")
        self.db.add_audit(ticket_id, "SESSION_OPENED", "Ticket session loaded")
        self.ticket_logger.for_ticket(ticket_id, self.ticket_paths['logs']).info("Session opened")

    def refresh_steps(self):
        self.steps = self.db.get_steps(self.ticket_id)
        self.step_list.delete(0, 'end')
        for step in self.steps:
            mark = "[DONE]" if step['status'] == 'COMPLETED' else "[PENDING]"
            self.step_list.insert('end', f"{mark} {step['step_number']}. {step['step_name']}")

    def select_step(self, _event=None):
        selection = self.step_list.curselection()
        if selection:
            self.show_step(self.steps[selection[0]])

    def show_step(self, step):
        self.current_step = step
        self.evidence_path = Path(step['screenshot_path']) if step.get('screenshot_path') else None
        self.status_label.config(text=f"Step {step['step_number']}: {step['step_name']} | {step['status']}")
        content = "Things to verify:\n\n" + "\n".join(f"• {idea}" for idea in step['ideas'])
        self.guidance.config(state='normal')
        self.guidance.delete('1.0', 'end')
        self.guidance.insert('1.0', content)
        self.guidance.config(state='disabled')
        self.evidence_label.config(text=f"Evidence: {self.evidence_path or 'Not selected'}")

    def _privacy_confirmed(self):
        if self.config_data.get('require_sanitized_evidence_confirmation', True) and not self.sanitized_var.get():
            raise ValidationError("Confirm that the evidence is sanitized before importing or capturing it.")

    def import_evidence(self):
        try:
            self._privacy_confirmed()
            if not self.current_step:
                raise ValidationError("Load a ticket and select the current pending step.")
            source = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
            if not source:
                return
            manager = ScreenshotManager(self.ticket_paths['screenshots'])
            self.evidence_path = manager.import_sanitized(source, self.current_step['step_number'])
            self.evidence_label.config(text=f"Evidence: {self.evidence_path}")
        except Exception as exc:
            messagebox.showerror("Evidence error", str(exc))

    def capture_screen(self):
        try:
            self._privacy_confirmed()
            if not self.current_step:
                raise ValidationError("Load a ticket and select the current pending step.")
            messagebox.showinfo("Screen capture", "The application will hide and capture the full screen after the configured delay. Ensure all sensitive data is masked.")
            self.withdraw()
            try:
                manager = ScreenshotManager(self.ticket_paths['screenshots'])
                self.evidence_path = manager.capture_full_screen(self.current_step['step_number'], self.config_data.get('screenshot_delay_seconds', 3))
            finally:
                self.deiconify()
            self.evidence_label.config(text=f"Evidence: {self.evidence_path}")
        except Exception as exc:
            self.deiconify()
            messagebox.showerror("Capture error", str(exc))

    def complete_step(self):
        try:
            if not self.current_step:
                raise ValidationError("No step is selected.")
            self._privacy_confirmed()
            self.validator.can_complete(self.steps, self.current_step['step_number'], self.evidence_path or '')
            self.db.complete_step(self.ticket_id, self.current_step['step_number'], self.evidence_path)
            self.ticket_logger.for_ticket(self.ticket_id, self.ticket_paths['logs']).info("Step %s completed", self.current_step['step_number'])
            self.sanitized_var.set(False)
            self.evidence_path = None
            self.refresh_steps()
            pending = self.validator.next_pending(self.steps)
            if pending:
                self.step_list.selection_clear(0, 'end')
                self.step_list.selection_set(pending['step_number'] - 1)
                self.show_step(pending)
            else:
                self.current_step = None
                self.status_label.config(text="All mandatory steps complete. Finalize the ticket.")
                self.evidence_label.config(text="Evidence: All evidence recorded")
            messagebox.showinfo("Step complete", "The step and evidence were recorded.")
        except Exception as exc:
            messagebox.showerror("Cannot complete step", str(exc))

    def finalize(self):
        try:
            if not self.ticket_id:
                raise ValidationError("Load a ticket first.")
            self.steps = self.db.get_steps(self.ticket_id)
            self.validator.can_close(self.steps)
            self.db.mark_ticket_completed(self.ticket_id)
            ticket = self.db.get_ticket(self.ticket_id)
            filename = f"{self.ticket_id}{self.config_data['report_filename_suffix']}"
            output = self.ticket_paths['report'] / filename
            self.report_generator.create_word_report(self.ticket_id, output)
            self.ticket_logger.for_ticket(self.ticket_id, self.ticket_paths['logs']).info("Report generated: %s", output)
            messagebox.showinfo("Ticket finalized", f"Report generated successfully:\n{output}")
            self.load_ticket(self.ticket_id)
        except Exception as exc:
            messagebox.showerror("Cannot finalize ticket", str(exc))
