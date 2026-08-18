"""Per-ticket plain-text activity logging."""
import logging
from datetime import datetime


class TicketLogger:
    def __init__(self):
        self._loggers = {}

    def for_ticket(self, ticket_id, log_dir):
        if ticket_id in self._loggers:
            return self._loggers[ticket_id]
        logger = logging.getLogger(f"ticket.{ticket_id}")
        logger.setLevel(logging.INFO)
        logger.propagate = False
        if not logger.handlers:
            handler = logging.FileHandler(log_dir / "activity.log", encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            logger.addHandler(handler)
        self._loggers[ticket_id] = logger
        return logger
