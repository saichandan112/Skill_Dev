from docx import Document
from docx.shared import Inches

def create_report(ticket_id,
                  checklist_data):

    doc = Document()

    doc.add_heading(
        f"{ticket_id}_analysis",
        level=1
    )

    for item in checklist_data:

        doc.add_heading(
            item["step"],
            level=2
        )

        doc.add_paragraph(
            "Status : Completed"
        )

        doc.add_picture(
            item["image"],
            width=Inches(5)
        )

    output = f"reports/{ticket_id}_analysis.docx"

    doc.save(output)

    return output   