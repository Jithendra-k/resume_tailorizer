import streamlit as st
from components.job_scraper import scrape_job
from components.resume_processor import process_resume
from components.pdf_generator import generate_pdf
from utils.db_utils import get_db_client, get_or_create_collection, add_documents
import uuid

def show():
    st.title("Tailor Your Resume")

    if 'resume_content' not in st.session_state:
        st.warning("Please upload your resume first on the 'Upload Resume' page.")
        return

    job_url = st.text_input("Enter the job posting URL:")

    if st.button("Tailor Resume"):
        if job_url:
            with st.spinner("Tailoring your resume..."):
                # Scrape job description
                job_data = scrape_job(job_url)

                if job_data:
                    # Store job description in ChromaDB
                    client = get_db_client()
                    collection = get_or_create_collection(client, "job_descriptions")
                    job_id = str(uuid.uuid4())
                    add_documents(collection, [job_data['description']], [{"url": job_url}], [job_id])

                    # Generate tailored resume
                    tailored_resume = process_resume(st.session_state['resume_content'], job_data['description'])

                    # Display results
                    st.subheader("Original Job Description")
                    st.write(job_data['description'])

                    st.subheader("Tailored Resume")
                    st.write(tailored_resume)

                    # Generate and offer PDF download
                    pdf = generate_pdf(tailored_resume)
                    st.download_button(
                        label="Download Tailored Resume as PDF",
                        data=pdf,
                        file_name="tailored_resume.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Failed to scrape job description. Please check the URL and try again.")
        else:
            st.error("Please provide a job URL.")