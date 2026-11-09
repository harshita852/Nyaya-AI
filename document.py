
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from io import BytesIO
from datetime import date


def generate_document(complaint):
    """
    Generate a formatted consumer complaint
    document in DOCX format.
    """

    doc = Document()

    # Page layout
    section = doc.sections[0]

    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    # Default font
    style = doc.styles["Normal"]

    style.font.name = "Arial"
    style.font.size = Pt(11)

    style.paragraph_format.space_after = Pt(8)

    # Document title
    title = doc.add_heading(
        "CONSUMER COMPLAINT",
        level=0
    )

    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for run in title.runs:
        run.font.color.rgb = RGBColor(31, 78, 121)
        run.font.size = Pt(20)

    # Date
    date_para = doc.add_paragraph()

    date_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    date_run = date_para.add_run(
        f"Date: {date.today().strftime('%d %B %Y')}"
    )

    date_run.bold = True

    # Recipient
    doc.add_heading("To", level=1)

    doc.add_paragraph(
        "The Customer Grievance Redressal Officer\n"
        "[Company Name]\n"
        "[Company Address]"
    )

    # Subject
    doc.add_heading("Subject", level=1)

    doc.add_paragraph(
        "Formal complaint regarding consumer grievance"
    )

    # Complaint body
    doc.add_heading("Complaint Details", level=1)

    for paragraph in complaint.split("\n"):

        if paragraph.strip():

            doc.add_paragraph(
                paragraph.strip()
            )

    # Closing
    doc.add_paragraph()

    doc.add_paragraph(
        "Regards,\n"
        "[Your Name]\n"
        "[Contact Details]\n"
        "[Email Address]"
    )

    # Footer
    footer = section.footer.paragraphs[0]

    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER

    footer_run = footer.add_run(
        "Generated using Nyaya AI | "
        "Please verify all details before submission"
    )

    footer_run.font.size = Pt(8)
    footer_run.font.color.rgb = RGBColor(128, 128, 128)

    # Export to memory
    buffer = BytesIO()

    doc.save(buffer)

    buffer.seek(0)

    return buffer
