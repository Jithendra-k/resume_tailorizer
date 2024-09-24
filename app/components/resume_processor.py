import PyPDF2
import re
from app.utils.llm_utils import llm_service

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
    sections = {
        'contact': re.findall(r'(?:Email|Phone|Address):\s*(.*)', resume_text),
        'education': re.findall(r'(?:Education|University|College).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
        'experience': re.findall(r'(?:Experience|Work History).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
        'skills': re.findall(r'(?:Skills|Expertise).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
        'projects': re.findall(r'(?:Projects).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
        'publications': re.findall(r'(?:Publications).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
        'certifications': re.findall(r'(?:Certifications|Awards).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
        'achievements': re.findall(r'(?:Achievements|Extracurriculars).*?:(.*?)(?:\n\n|\Z)', resume_text, re.DOTALL),
    }
    return sections

def tailor_resume(resume_sections, job_description):
    """
    Use the LLM to tailor the resume based on the job description.
    """
    prompt = f"""
    Given the following resume sections and job description, 
    create a tailored resume that highlights relevant skills and experiences.
    Format the content to fit the following LaTeX template structure:

    \\documentclass[10pt,letterpaper]{{article}}
    \\usepackage[T1]{{fontenc}}
    \\usepackage[utf8]{{inputenc}}
    \\usepackage[margin=0.5in]{{geometry}}
    \\usepackage{{hyperref}}
    \\usepackage{{fontawesome5}}
    \\usepackage{{titlesec}}
    \\usepackage{{enumitem}}
    \\usepackage{{array}}
    \\usepackage{{setspace}}    
    \\usepackage{{makecell}} 
    \\setlength{{\\tabcolsep}}{{0pt}}


    \\titleformat{{\\section}}{{\\large\\bfseries}}{{\\thesection}}{{1em}}{{}}[\\titlerule]
    \\titlespacing*{{\\section}}{{0pt}}{{*1}}{{*0.5}}

    \\newcommand{{\\entry}}[2]{{
        \\noindent\\textbf{{#1}} \\hfill #2 \\\\[-0.5em]
    }}

    \\newcommand{{\\subentrywithdate}}[3]{{
        \\noindent\\textbf{{#1}} | #2 \\hfill #3 \\\\[-0.5em]
    }}

    \\newcommand{{\\subentry}}[2]{{
        \\noindent\\textbf{{#1}} | #2 \\\\[-0.5em]
    }}

    \\pagestyle{{empty}}
    \\setlength{{\\parindent}}{{0pt}}
    \\setstretch{{0.9}}

    \\begin{{document}}

    \\begin{{center}}
    \\begin{{tabular}}{{@{{}}p{{0.3\\textwidth}}@{{}} p{{0.4\\textwidth}}@{{}} p{{0.3\\textwidth}}@{{}}}}
    \\makecell[l]{{\\faPhone\\ (Phone) \\\\ \\faEnvelope\\ \\href{{mailto:email}}{{email}}}} &
    \\centering\\makecell[c]{{\\Large\\textbf{{Name}} \\\\ \\faLinkedin\\ \\href{{LinkedIn URL}}{{LinkedIn}}}} &
    \\makecell[r]{{Location \\\\ \\faGithub\\ \\href{{GitHub URL}}{{GitHub}}}} \\\\
    \\end{{tabular}}
    \\end{{center}}

    \\section*{{\\small EDUCATION}}
    \\makecell[l]{{University Name}}  \\centering
    \\makecell[c]{{Degree - GPA}}
    \\makecell[r]{{Date Range}} \\\\

    \\section*{{\\small EXPERIENCE}}
    \\subentrywithdate{{Company Name}}{{Position, Location}}{{Date Range}}
    \\begin{{itemize}}[leftmargin=*,noitemsep,topsep=0pt,parsep=0pt]
        \\item Achievement or responsibility
        \\item Achievement or responsibility
    \\end{{itemize}}

    \\section*{{\\small PROJECTS}}
    \\subentrywithdate{{Project Name}}{{Project Type}}{{Date Range}}
    \\begin{{itemize}}[leftmargin=*,noitemsep,topsep=0pt,parsep=0pt]
        \\item Project detail
        \\item Project detail
    \\end{{itemize}}

    \\section*{{\\small SKILLS}}
    \\begin{{tabular}}{{@{{}}p{{0.15\\textwidth}}@{{}} p{{0.85\\textwidth}}@{{}}}}
    \\textbf{{Skill Category:}} & Skill 1, Skill 2, Skill 3 \\\\
    \\end{{tabular}}

    \\section*{{\\small PUBLICATIONS}}
    \\begin{{itemize}}[leftmargin=*,noitemsep,topsep=0pt,parsep=0pt]
        \\item Publication detail \\hfill Date
    \\end{{itemize}}

    \\section*{{\\small CERTIFICATIONS/AWARDS}}
    \\begin{{enumerate}}[leftmargin=*,noitemsep,topsep=0pt,parsep=0pt]
        \\item Certification or Award detail \\hfill Date Range
    \\end{{enumerate}}

    \\section*{{\\small ACHIEVEMENTS/EXTRACURRICULARS}}
    \\begin{{itemize}}[leftmargin=*,noitemsep,topsep=0pt,parsep=0pt]
        \\item Achievement or extracurricular activity
    \\end{{itemize}}

    \\end{{document}}

    Resume Sections:
    {resume_sections}

    Job Description:
    {job_description}

    Provide the tailored resume content in LaTeX format, following the structure above. 
    Ensure all special characters are properly escaped for LaTeX.
    """
    return llm_service.process(prompt)

    return llm_service.process(prompt)

def process_resume(resume_content, job_description):
    """
    Main function to process the resume and tailor it to the job description.
    """
    parsed_resume = parse_resume(resume_content)
    tailored_resume = tailor_resume(parsed_resume, job_description)
    return tailored_resume