import requests
from bs4 import BeautifulSoup
import re


def scrape_job(url):
    """
    Scrape job details from the given URL.
    This is a basic implementation and may need to be adjusted based on the specific websites you're targeting.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # These selectors are examples and may need to be adjusted
        title = soup.find('h1', class_='job-title').text.strip()
        company = soup.find('div', class_='company-name').text.strip()
        description = soup.find('div', class_='job-description').text.strip()

        # Clean up the description
        description = re.sub(r'\s+', ' ', description)

        return {
            'title': title,
            'company': company,
            'description': description,
            'url': url
        }
    except Exception as e:
        print(f"Error scraping job: {e}")
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