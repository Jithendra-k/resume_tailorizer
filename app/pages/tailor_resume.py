import streamlit as st
from app.components.job_scraper import scrape_job
from app.components.resume_processor import process_resume
from app.components.pdf_generator import generate_pdf, test_latex
from app.utils.db_utils import get_db_client, get_or_create_collection, add_documents
import uuid
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def show():
    st.title("Tailor Your Resume")

    if 'resume_content' not in st.session_state:
        st.warning("Please upload your resume first on the 'Upload Resume' page.")
        return

    # Initialize session state variables
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'tailored_resume' not in st.session_state:
        st.session_state.tailored_resume = ""

    job_url = st.text_input("Enter the job posting URL:")
    job_description_manual = st.text_area("Or paste the job description here:")

    if st.button("Tailor Resume"):
        if job_url or job_description_manual:
            with st.spinner("Tailoring your resume..."):
                if job_url:
                    job_data = scrape_job(job_url)
                    if not job_data:
                        st.error("Failed to scrape job description. Please check the URL and try again.")
                        return
                    st.session_state.job_description = job_data['description']
                else:
                    st.session_state.job_description = job_description_manual

                # Store job description in ChromaDB
                client = get_db_client()
                collection = get_or_create_collection(client, "job_descriptions")
                job_id = str(uuid.uuid4())
                add_documents(collection, [st.session_state.job_description], [{"url": job_url or "Manual Entry"}],
                              [job_id])

                try:
                    # Generate tailored resume
                    st.session_state.tailored_resume = process_resume(st.session_state.resume_content,
                                                                      st.session_state.job_description)
                except Exception as e:
                    logger.error(f"Error processing resume: {str(e)}")
                    st.error(
                        "An error occurred while processing your resume. Please try again later or contact support.")
                    return

    if st.session_state.job_description:
        st.subheader("Job Description")
        st.write(st.session_state.job_description)

    if st.session_state.tailored_resume:
        st.subheader("Tailored Resume (LaTeX format)")
        edited_resume = st.text_area("Edit your tailored resume (LaTeX format)", st.session_state.tailored_resume,
                                     height=400)

        if st.button("Update Resume"):
            st.session_state.tailored_resume = edited_resume
            st.success("Resume updated successfully!")

        if st.button("Generate PDF"):
            try:
                with st.spinner("Generating PDF... This may take a few moments."):
                    start_time = time.time()
                    pdf_bytes = generate_pdf(st.session_state.tailored_resume)
                    end_time = time.time()

                    logger.info(f"PDF generation took {end_time - start_time:.2f} seconds")

                    if pdf_bytes:
                        st.success("PDF generated successfully!")
                        st.download_button(
                            label="Download Tailored Resume as PDF",
                            data=pdf_bytes,
                            file_name="tailored_resume.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("PDF generation failed. Please try again or contact support.")
            except Exception as e:
                logger.error(f"Error generating PDF: {str(e)}")
                st.error(f"An error occurred while generating the PDF: {str(e)}")

        if st.button("Display Raw LaTeX"):
            st.code(st.session_state.tailored_resume, language="tex")

        if st.button("Test LaTeX"):
            try:
                test_latex()
                st.success("Test PDF generated successfully. Check your application directory for 'test.pdf'.")
            except Exception as e:
                st.error(f"Error generating test PDF: {str(e)}")

    st.markdown("---")
    st.subheader("Troubleshooting")
    st.markdown("""
    If you're having trouble:
    1. Make sure the job URL is correct and accessible.
    2. If using Ollama, ensure you have pulled the llama2 model by running `ollama pull llama2` in your terminal.
    3. Check your internet connection.
    4. If problems persist, try pasting the job description manually instead of using the URL.
    5. If you continue to experience issues, please contact support.
    """)