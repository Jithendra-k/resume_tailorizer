import subprocess
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_pdf(latex_content):
    logger.info("Starting PDF generation")
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        with open(tex_path, "w", encoding='utf-8') as tex_file:
            tex_file.write(latex_content)

        logger.info(f"LaTeX file written to {tex_path}")

        # Run pdflatex twice to ensure all references are resolved
        for i in range(2):
            logger.info(f"Running pdflatex (attempt {i + 1})")
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", tmpdir, tex_path],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                logger.error(f"LaTeX compilation failed. Error output:\n{result.stdout}\n{result.stderr}")
                with open(tex_path, 'r', encoding='utf-8') as f:
                    logger.error(f"LaTeX content:\n{f.read()}")
                raise Exception(f"LaTeX compilation failed. See log for details.")

        pdf_path = os.path.join(tmpdir, "resume.pdf")
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found at expected path: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found at expected path: {pdf_path}")

        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()

    logger.info("PDF generation completed successfully")
    return pdf_bytes


def save_pdf(latex_content, filename):
    """
    Save the generated PDF to a file.
    """
    pdf_bytes = generate_pdf(latex_content)
    with open(filename, 'wb') as f:
        f.write(pdf_bytes)
    print(f"PDF saved as {filename}")


def test_latex():
    simple_latex = r"""
    \documentclass{article}
    \begin{document}
    Hello, World!
    \end{document}
    """
    try:
        pdf_bytes = generate_pdf(simple_latex)
        with open("test.pdf", "wb") as f:
            f.write(pdf_bytes)
        print("Test PDF generated successfully")
    except Exception as e:
        print(f"Error generating test PDF: {str(e)}")
        raise