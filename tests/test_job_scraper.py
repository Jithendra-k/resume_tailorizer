import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from app.components.job_scraper import scrape_job, extract_skills


class TestJobScraper(unittest.TestCase):

    @patch('components.job_scraper.requests.get')
    def test_scrape_job(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <h1 class="job-title">Software Engineer</h1>
            <div class="company-name">TechCorp</div>
            <div class="job-description">We are looking for a Python developer with experience in web scraping and API development.</div>
        </html>
        '''
        mock_get.return_value = mock_response

        result = scrape_job('https://example.com/job')

        self.assertEqual(result['title'], 'Software Engineer')
        self.assertEqual(result['company'], 'TechCorp')
        self.assertIn('Python developer', result['description'])

    def test_extract_skills(self):
        job_description = "We need a developer with skills in Python, Java, and SQL. Experience with machine learning is a plus."
        skills = extract_skills(job_description)

        self.assertIn('python', skills)
        self.assertIn('java', skills)
        self.assertIn('sql', skills)
        self.assertIn('machine learning', skills)
        self.assertNotIn('c++', skills)


if __name__ == '__main__':
    unittest.main()