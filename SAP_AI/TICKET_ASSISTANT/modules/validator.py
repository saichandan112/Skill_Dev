"""Input, ordering, evidence, and closure validation."""
import re
from pathlib import Path


class ValidationError(Exception):
    pass


class Validator:
    def __init__(self, ticket_pattern):
        self.ticket_pattern = re.compile(ticket_pattern)

    def ticket_id(self, value):
        normalized = value.strip().upper()
        if not self.ticket_pattern.fullmatch(normalized):
            raise ValidationError("Ticket ID must contain 2-10 letters followed by 3-12 digits, for example INC123456.")
        return normalized

    @staticmethod
    def next_pending(steps):
        return next((s for s in steps if s['status'] != 'COMPLETED'), None)

    def can_complete(self, steps, requested_step_number, screenshot_path):
        pending = self.next_pending(steps)
        if not pending:
            raise ValidationError("All steps are already complete.")
        if pending['step_number'] != requested_step_number:
            raise ValidationError(f"Step skipping is not allowed. Complete step {pending['step_number']} first.")
        evidence = Path(screenshot_path)
        if not evidence.exists() or evidence.stat().st_size == 0:
            raise ValidationError("A valid evidence image is mandatory before completing the step.")
        return True

    def can_close(self, steps):
        pending = [s for s in steps if s['status'] != 'COMPLETED']
        if pending:
            numbers = ", ".join(str(s['step_number']) for s in pending)
            raise ValidationError(f"Pending steps found: {numbers}. The report cannot be finalized.")
        return True
