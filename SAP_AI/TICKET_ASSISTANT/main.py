"""Entry point for SAP AI Ticket Assistant MVP."""
from modules.ui import TicketAssistantApp


def main():
    app = TicketAssistantApp()
    app.mainloop()


if __name__ == "__main__":
    main()
