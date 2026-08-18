import tkinter as tk
from tkinter import ttk
from modules.checklist import load_checklist

def start_ui():

    root = tk.Tk()

    root.title(
        "Ticket Resolution Assistant"
    )

    tk.Label(
        root,
        text="Ticket ID"
    ).pack()

    ticket = tk.Entry(root)
    ticket.pack()

    tk.Label(
        root,
        text="Issue Type"
    ).pack()

    combo = ttk.Combobox(
        root,
        values=[
            "RegWeb",
            "W4 Forms",
            "Job Failure",
            "YTD"
        ]
    )

    combo.pack()

    root.mainloop()