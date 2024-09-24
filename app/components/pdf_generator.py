from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO


def generate_pdf(content):
    """
    Generate a PDF document from the given content.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    flowables = []

    # Split the content into lines
    lines = content.split('\n')

    for line in lines:
        p = Paragraph(line, styles["Normal"])
        flowables.append(p)
        flowables.append(Spacer(1, 12))

    doc.build(flowables)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def save_pdf(content, filename):
    """
    Save the generated PDF to a file.
    """
    pdf = generate_pdf(content)
    with open(filename, 'wb') as f:
        f.write(pdf)
    print(f"PDF saved as {filename}")