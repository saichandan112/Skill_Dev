"""Completion summary and final report orchestration."""
from pathlib import Path


class ReportGenerator:
    def __init__(self, database, document_generator):
        self.database = database
        self.document_generator = document_generator

    @staticmethod
    def summary(steps):
        total = len(steps)
        completed = sum(1 for step in steps if step['status'] == 'COMPLETED')
        return {"total": total, "completed": completed, "pending": total - completed}

    def create_word_report(self, ticket_id, output_path):
        ticket = self.database.get_ticket(ticket_id)
        steps = self.database.get_steps(ticket_id)
        audits = self.database.audit_events(ticket_id)
        return self.document_generator.generate(ticket, steps, audits, Path(output_path))
