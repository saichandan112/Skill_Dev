"""Ticket folder creation and resume support."""
from pathlib import Path


class SessionManager:
    def __init__(self, data_root):
        self.data_root = Path(data_root)
        self.data_root.mkdir(parents=True, exist_ok=True)

    def ticket_paths(self, ticket_id):
        base = self.data_root / ticket_id
        paths = {
            "base": base,
            "screenshots": base / "screenshots",
            "logs": base / "logs",
            "report": base / "report",
            "exports": base / "exports",
        }
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)
        return paths
