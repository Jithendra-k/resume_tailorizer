import PyPDF2
import re
from utils.llm_utils import llm_service


def extract_text_from_pdf(pdf_file):
    """
    Extract text content from a PDF file.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def parse_resume(resume_text):
    """
    Parse the resume text to extract relevant information.
    This is a basic implementation and can be improved with more sophisticated NLP techniques.
    """
    # Extract sections (very basic implementation)
    sections = {
        'contact': re.findall(r'(?:Email|Phone|Address):\s*(.*)', resume_text),
        'education': re.findall(r'(?:Education|University|College).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
        'experience': re.findall(r'(?:Experience|Work History).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
        'skills': re.findall(r'(?:Skills|Expertise).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
    }

    return sections


def tailor_resume(resume_sections, job_description):
    """
    Use the LLM to tailor the resume based on the job description.
    """
    prompt = f"""
    Given the following resume sections and job description, 
    create a tailored resume that highlights relevant skills and experiences:

    Resume:
    {resume_sections}

    Job Description:
    {job_description}

    Provide the tailored resume content, maintaining a professional structure:
    """
    return llm_service.process(prompt)


def process_resume(resume_content, job_description):
    """
    Main function to process the resume and tailor it to the job description.
    """
    parsed_resume = parse_resume(resume_content)
    tailored_resume = tailor_resume(parsed_resume, job_description)
    return tailored_resume