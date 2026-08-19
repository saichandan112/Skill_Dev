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