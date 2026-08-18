# SAP AI Ticket Assistant

## 1. Overview

SAP AI Ticket Assistant is a local Python desktop application that guides support engineers through mandatory ticket-resolution steps. It prevents step skipping, requires sanitized evidence for every completed step, maintains an audit trail, resumes interrupted tickets, and generates a Microsoft Word evidence report.

Despite the product name, the MVP does **not** use an AI model and does not connect to SAP. Its intelligence comes from configurable guided checklists. AI recommendations may be introduced later only after privacy, information-security, and architecture approval.

## 2. Business Goals

The tool is designed to:

- Standardize ticket resolution across engineers.
- Prevent mandatory checks from being missed.
- Guide investigation without directly reading SAP data.
- Require evidence before a checklist step can be completed.
- Maintain ticket-level SQLite and text audit logs.
- Resume in-progress tickets after the application is closed.
- Generate a Word report containing the checklist and evidence.
- Support non-Python users through a packaged Windows application.

## 3. Privacy and Compliance Boundary

This application does not connect to SAP, databases, service APIs, Outlook, or Teams. It records only:

- Ticket ID
- Ticket type
- Step number and name
- Completion state and timestamp
- Local evidence file path
- Technical audit events

### Critical limitation

A screenshot can contain production or personal data if the user captures it. Software cannot guarantee that an arbitrary screenshot is safe. Therefore:

1. Live capture is disabled by default.
2. The preferred workflow is to import a pre-sanitized screenshot.
3. The user must confirm that evidence is sanitized.
4. Evidence should never include employee data, payroll values, tax information, interface payloads, credentials, database records, or other business content.
5. Retention, deletion, access control, encryption, and sharing must follow the organization's policies.

To enable optional full-screen capture after formal approval, edit `config/app_config.json`:

```json
"allow_live_screenshot_capture": true
```

The live-capture feature hides the application, waits for the configured delay, and captures the full screen. It must not be enabled unless the environment and process make sensitive-data exposure impossible or properly controlled.

## 4. Main Workflow

```text
Open Tool
  -> Enter Ticket ID
  -> Select Ticket Type
  -> Start New or Resume
  -> Load Dynamic Checklist
  -> Review Guided Checks
  -> Import Sanitized Evidence
  -> Confirm Evidence Is Sanitized
  -> Complete Current Mandatory Step
  -> Repeat in Sequence
  -> Validate All Steps
  -> Generate Word Report
  -> Mark Ticket Completed
```

## 5. Project Structure

```text
SAP_AI_TICKET_ASSISTANT/
|-- main.py
|-- requirements.txt
|-- README.md
|-- setup_windows.bat
|-- run_windows.bat
|-- build_exe.bat
|-- config/
|   |-- app_config.json
|   `-- checklist_templates.json
|-- modules/
|   |-- __init__.py
|   |-- config.py
|   |-- checklist.py
|   |-- database.py
|   |-- document_generator.py
|   |-- logger.py
|   |-- report_generator.py
|   |-- screenshot.py
|   |-- screenshot_manager.py
|   |-- session_manager.py
|   |-- validator.py
|   `-- ui.py
|-- tests/
|   `-- test_validator.py
|-- TicketData/
|-- reports/
|-- screenshots/
|-- logs/
|-- exports/
`-- assets/
```

Runtime output for a ticket:

```text
TicketData/
|-- ticket_assistant.db
`-- INC123456/
    |-- screenshots/
    |   |-- step_01.png
    |   `-- step_02.png
    |-- logs/
    |   `-- activity.log
    |-- report/
    |   `-- INC123456_analysis.docx
    `-- exports/
```

## 6. Module Responsibilities

- `main.py`: Application entry point.
- `modules/config.py`: Resolves development and packaged-application paths.
- `modules/checklist.py`: Loads and validates JSON checklist templates.
- `modules/database.py`: Creates SQLite tables and stores tickets, steps, and audit events.
- `modules/validator.py`: Validates ticket IDs, prevents step skipping, requires evidence, and blocks premature closure.
- `modules/session_manager.py`: Creates ticket folders and supports resume behavior.
- `modules/screenshot_manager.py`: Imports sanitized PNG/JPEG evidence and optionally captures the screen.
- `modules/logger.py`: Writes a plain-text `activity.log` for each ticket.
- `modules/document_generator.py`: Creates the final `.docx` evidence report.
- `modules/report_generator.py`: Coordinates report data and document generation.
- `modules/ui.py`: Implements the Tkinter desktop interface.

## 7. Prerequisites

For development:

- Windows 10 or Windows 11
- Python 3.10 or later
- Permission to create folders and SQLite files
- Microsoft Word or another DOCX-compatible viewer for opening generated reports

Tkinter is normally included with the standard Windows Python installer. During Python installation, select **Add Python to PATH**.

## 8. Quick Start on Windows

### Automated setup

1. Extract the project ZIP.
2. Open the extracted `SAP_AI_TICKET_ASSISTANT` folder.
3. Double-click `setup_windows.bat`.
4. After setup succeeds, double-click `run_windows.bat`.

The setup script creates `.venv`, installs dependencies, and runs tests.

### Manual setup

Open Command Prompt in the project directory:

```bat
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m unittest discover -s tests -v
python main.py
```

## 9. How to Use the Application

1. Enter a ticket ID such as `INC123456`.
2. Select the ticket type.
3. Click **Start New**.
4. Review the first mandatory step and its troubleshooting guidance.
5. Create a sanitized screenshot using an approved process.
6. Select the privacy confirmation checkbox.
7. Click **Import Sanitized Screenshot**.
8. Click **Complete Current Step**.
9. Continue through all steps in order.
10. Click **Finalize and Generate Word Report**.
11. Open the report under `TicketData/<TICKET_ID>/report/`.
12. To continue an interrupted ticket, enter its ID and click **Resume**.

## 10. Checklist Customization

Edit `config/checklist_templates.json`. Each ticket type contains ordered step objects:

```json
{
  "Job Failure": [
    {
      "step": "Check Job Logs",
      "ideas": [
        "Review the job log",
        "Check runtime errors",
        "Review sanitized spool status"
      ]
    }
  ]
}
```

Rules:

- Each ticket type must have at least one step.
- Every step requires a non-empty `step` value.
- `ideas` must be a JSON list.
- Step order in the JSON file is the enforced completion order.
- Restart the application after updating templates.
- Existing tickets retain the checklist version saved when they were created.

## 11. Application Configuration

`config/app_config.json` controls:

- Application name and version
- Data and database locations
- Screenshot capture policy
- Sanitized-evidence confirmation
- Capture delay
- Ticket ID format
- Report file suffix
- Organization name

Use relative paths to keep deployment portable. Back up the `TicketData` directory before changing storage settings.

## 12. Database Design

SQLite database: `TicketData/ticket_assistant.db`

### `tickets`

- `ticket_id`
- `issue_type`
- `created_at`
- `updated_at`
- `status`

### `steps`

- `ticket_id`
- `step_number`
- `step_name`
- `guidance_json`
- `status`
- `screenshot_path`
- `completed_at`

### `audit_events`

- `id`
- `ticket_id`
- `event_type`
- `details`
- `occurred_at`

The database stores paths to evidence. The actual image files remain in the ticket folder.

## 13. Word Report Contents

The generated report includes:

- Ticket ID and issue type
- Status and timestamps
- Privacy notice
- Every ordered resolution step
- Step completion timestamp
- Guided checks
- Associated screenshot
- Evidence filename
- Audit-event table

The report is generated only after every mandatory step is completed.

## 14. Build the Windows Application

Run:

```bat
build_exe.bat
```

The distributable application is created under:

```text
dist\SAP_AI_Ticket_Assistant\SAP_AI_Ticket_Assistant.exe
```

This project intentionally uses PyInstaller's folder-based deployment rather than `--onefile`. Folder-based packaging makes the JSON configuration editable and is generally easier to troubleshoot. Distribute the complete `dist\SAP_AI_Ticket_Assistant` folder, not only the EXE.

Before enterprise distribution:

- Add an approved icon and product metadata.
- Code-sign the executable.
- Scan the build with enterprise endpoint-security tools.
- Test on a clean managed workstation.
- Confirm write permissions for the deployment/data location.
- Obtain privacy, security, legal, and support-process approval.
- Define backup, retention, archival, and deletion policies.

## 15. Tests

Run validation tests:

```bat
.venv\Scripts\activate
python -m unittest discover -s tests -v
```

Current tests cover ticket ID normalization, step-skipping prevention, and closure blocking when steps are pending. Add database, document-generation, UI, corruption-recovery, and packaging tests before production adoption.

## 16. Troubleshooting

### `py` is not recognized

Install Python from the approved organizational software source and select **Add Python to PATH**, or replace `py -3` in the setup script with the approved Python executable.

### Screenshot import fails

Confirm the source file is an existing PNG or JPEG and is not corrupted. Copy it to a local approved directory and retry.

### Word report is not generated

Confirm every step displays `[DONE]`, evidence files still exist, and the application has write permission to the ticket report folder.

### Application cannot resume a ticket

Confirm the same `TicketData/ticket_assistant.db` file is being used and the ticket ID format is correct.

### EXE configuration is missing

Keep the complete generated distribution folder together. The `config` directory must be beside the packaged application files.

## 17. Security Recommendations Before Production Use

This MVP is a functional starter project, not a final enterprise security product. Recommended controls include:

- Store data only in an approved encrypted location.
- Restrict ticket folders using operating-system access controls.
- Add authenticated user identity from an approved corporate source.
- Add hash values for evidence and generated reports to detect changes.
- Add tamper-evident or centralized audit logging.
- Add automated retention and secure deletion.
- Disable arbitrary paths if using a centrally managed storage location.
- Add malware scanning for imported images.
- Add screenshot preview and approved redaction capability.
- Require a separate approval before enabling live screen capture.
- Conduct threat modeling, privacy review, penetration testing, and user acceptance testing.

## 18. Known MVP Limitations

- No direct SAP integration.
- No AI model or automated recommendations.
- No automated screenshot redaction.
- Local SQLite database only.
- No user authentication or role-based access control.
- No cryptographic evidence integrity check.
- No Teams, Outlook, PDF, or dashboard integration.
- No centralized deployment or update mechanism.
- Reports can become large when screenshots are high resolution.

## 19. Suggested Version 2 Roadmap

1. Evidence preview and manual redaction.
2. Evidence hashing and tamper-evident manifests.
3. Role-based access and corporate identity.
4. Approved centralized storage and audit service.
5. Dashboard for completion and aging statistics.
6. PDF export.
7. Teams and Outlook integration through approved APIs.
8. Digitally signed reports.
9. Versioned checklist governance and approval workflow.
10. AI recommendations based only on approved, non-production knowledge sources.

## 20. Acceptance Criteria

The MVP is accepted when:

- A valid ticket can be created.
- A ticket-type checklist loads dynamically.
- Steps cannot be completed out of order.
- A step cannot be completed without an evidence image.
- An interrupted ticket can be resumed.
- SQLite and text audit logs are created.
- Ticket-specific folders are created automatically.
- Closure is blocked while any step is pending.
- A DOCX report is generated after all steps complete.
- The application can be packaged and run on a clean Windows test workstation.

## 21. Ownership and Governance

Assign named owners for:

- Product and process ownership
- Checklist content approval
- Application support
- Information security
- Privacy and compliance
- Data retention and deletion
- Release management

Checklist changes should be reviewed, versioned, tested, and approved before deployment.
