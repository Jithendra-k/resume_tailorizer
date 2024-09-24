import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.components.pdf_generator import generate_pdf, save_pdf


class TestPDFGenerator(unittest.TestCase):

    def test_generate_pdf(self):
        content = "Test resume content"
        pdf = generate_pdf(content)

        self.assertIsInstance(pdf, bytes)
        self.assertTrue(pdf.startswith(b'%PDF'))  # PDF files start with this signature

    def test_save_pdf(self):
        content = "Test resume content"
        filename = "test_resume.pdf"

        save_pdf(content, filename)

        self.assertTrue(os.path.exists(filename))

        # Clean up the test file
        os.remove(filename)


if __name__ == '__main__':
    unittest.main()