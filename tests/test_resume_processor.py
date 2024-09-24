import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from app.components.resume_processor import parse_resume, tailor_resume, process_resume


class TestResumeProcessor(unittest.TestCase):

    def test_parse_resume(self):
        resume_text = '''
        John Doe
        Email: john@example.com
        Phone: 123-456-7890

        Education:
        Bachelor of Science in Computer Science, University of Example

        Experience:
        Software Developer at TechCorp
        - Developed web applications using Python and Django
        - Implemented RESTful APIs

        Skills:
        Python, JavaScript, SQL, Git
        '''

        parsed_resume = parse_resume(resume_text)

        self.assertIn('john@example.com', parsed_resume['contact'])
        self.assertIn('Bachelor of Science', parsed_resume['education'][0])
        self.assertIn('Software Developer', parsed_resume['experience'][0])
        self.assertIn('Python', parsed_resume['skills'][0])

    @patch('components.resume_processor.llm_service.process')
    def test_tailor_resume(self, mock_llm_process):
        mock_llm_process.return_value = "Tailored resume content"

        resume_sections = {
            'contact': ['john@example.com'],
            'education': ['BS in Computer Science'],
            'experience': ['Software Developer at TechCorp'],
            'skills': ['Python, JavaScript, SQL']
        }
        job_description = "We are looking for a Python developer"

        result = tailor_resume(resume_sections, job_description)

        self.assertEqual(result, "Tailored resume content")
        mock_llm_process.assert_called_once()

    @patch('components.resume_processor.parse_resume')
    @patch('components.resume_processor.tailor_resume')
    def test_process_resume(self, mock_tailor, mock_parse):
        mock_parse.return_value = {'parsed': 'resume'}
        mock_tailor.return_value = "Tailored resume"

        result = process_resume("Original resume", "Job description")

        self.assertEqual(result, "Tailored resume")
        mock_parse.assert_called_once_with("Original resume")
        mock_tailor.assert_called_once()


if __name__ == '__main__':
    unittest.main()