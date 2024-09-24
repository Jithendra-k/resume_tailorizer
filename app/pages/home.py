import streamlit as st


def show():
    st.title("Welcome to Resume Tailorizer")
    st.write("""
    Resume Tailorizer helps you customize your resume for specific job postings.
    Here's how it works:
    1. Upload your resume or enter your resume text
    2. Provide a job posting URL
    3. Our AI will tailor your resume to match the job requirements
    4. Review and download your tailored resume

    Get started by navigating to the 'Tailor Resume' page!
    """)

    st.image("https://via.placeholder.com/600x400.png?text=Resume+Tailorizer", caption="Resume Tailorizer Process")