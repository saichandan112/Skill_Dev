"""SQLite persistence layer."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Database:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def initialize(self):
        with self.connect() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                issue_type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('IN_PROGRESS','COMPLETED'))
            );
            CREATE TABLE IF NOT EXISTS steps (
                ticket_id TEXT NOT NULL,
                step_number INTEGER NOT NULL,
                step_name TEXT NOT NULL,
                guidance_json TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('PENDING','COMPLETED')),
                screenshot_path TEXT,
                completed_at TEXT,
                PRIMARY KEY(ticket_id, step_number),
                FOREIGN KEY(ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                details TEXT NOT NULL,
                occurred_at TEXT NOT NULL
            );
            """)

    def ticket_exists(self, ticket_id):
        with self.connect() as conn:
            return conn.execute("SELECT 1 FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone() is not None

    def create_ticket(self, ticket_id, issue_type, checklist):
        import json
        now = utc_now()
        with self.connect() as conn:
            conn.execute("INSERT INTO tickets VALUES (?, ?, ?, ?, 'IN_PROGRESS')", (ticket_id, issue_type, now, now))
            conn.executemany(
                "INSERT INTO steps VALUES (?, ?, ?, ?, 'PENDING', NULL, NULL)",
                [(ticket_id, i, item['step'], json.dumps(item.get('ideas', [])),) for i, item in enumerate(checklist, 1)]
            )
        self.add_audit(ticket_id, "TICKET_CREATED", f"Issue type: {issue_type}")

    def get_ticket(self, ticket_id):
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
            return dict(row) if row else None

    def get_steps(self, ticket_id):
        import json
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM steps WHERE ticket_id=? ORDER BY step_number", (ticket_id,)).fetchall()
        output = []
        for row in rows:
            item = dict(row)
            item['ideas'] = json.loads(item.pop('guidance_json'))
            output.append(item)
        return output

    def complete_step(self, ticket_id, step_number, screenshot_path):
        now = utc_now()
        with self.connect() as conn:
            conn.execute("UPDATE steps SET status='COMPLETED', screenshot_path=?, completed_at=? WHERE ticket_id=? AND step_number=?",
                         (str(screenshot_path), now, ticket_id, step_number))
            conn.execute("UPDATE tickets SET updated_at=? WHERE ticket_id=?", (now, ticket_id))
        self.add_audit(ticket_id, "STEP_COMPLETED", f"Step {step_number}; evidence={screenshot_path}")

    def mark_ticket_completed(self, ticket_id):
        now = utc_now()
        with self.connect() as conn:
            conn.execute("UPDATE tickets SET status='COMPLETED', updated_at=? WHERE ticket_id=?", (now, ticket_id))
        self.add_audit(ticket_id, "TICKET_COMPLETED", "All mandatory steps completed")

    def add_audit(self, ticket_id, event_type, details):
        with self.connect() as conn:
            conn.execute("INSERT INTO audit_events(ticket_id,event_type,details,occurred_at) VALUES (?,?,?,?)",
                         (ticket_id, event_type, details, utc_now()))

    def audit_events(self, ticket_id):
        with self.connect() as conn:
            return [dict(r) for r in conn.execute("SELECT * FROM audit_events WHERE ticket_id=? ORDER BY id", (ticket_id,)).fetchall()]
