import requests
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_job(url):
    """
    Scrape job details from the given URL.
    This is a basic implementation and may need to be adjusted based on the specific websites you're targeting.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try different selectors for job title
        title_selectors = ['h1.job-title', 'h1.posting-title', 'h1.title', 'h1']
        title = None
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.text.strip()
                break

        # Try different selectors for company name
        company_selectors = ['.company-name', '.organization-name', '.employer']
        company = None
        for selector in company_selectors:
            company_elem = soup.select_one(selector)
            if company_elem:
                company = company_elem.text.strip()
                break

        # Try different selectors for job description
        description_selectors = ['.job-description', '.description', '#job-description']
        description = None
        for selector in description_selectors:
            description_elem = soup.select_one(selector)
            if description_elem:
                description = description_elem.text.strip()
                break

        # If we couldn't find the description, try to get all text from the body
        if not description:
            body = soup.find('body')
            if body:
                description = body.text.strip()

        # Clean up the description
        if description:
            description = re.sub(r'\s+', ' ', description)

        if not (title and description):
            logger.error(f"Failed to extract job details from {url}")
            return None

        return {
            'title': title or "Unknown Title",
            'company': company or "Unknown Company",
            'description': description,
            'url': url
        }
    except Exception as e:
        logger.error(f"Error scraping job from {url}: {str(e)}")
        return None


def extract_skills(job_description):
    """
    Extract skills from the job description using a simple keyword matching approach.
    This is a basic implementation and can be improved with NLP techniques.
    """
    # This is a very basic list of skills. You should expand this based on your needs.
    common_skills = ['python', 'java', 'c++', 'javascript', 'react', 'node.js', 'sql', 'machine learning',
                     'data analysis']

    found_skills = []
    for skill in common_skills:
        if skill.lower() in job_description.lower():
            found_skills.append(skill)

    return found_skills