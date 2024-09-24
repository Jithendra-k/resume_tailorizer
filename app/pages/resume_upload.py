import streamlit as st
from components.resume_processor import extract_text_from_pdf

def show():
    st.title("Upload Your Resume")

    resume_option = st.radio("Choose resume input method:", ["Text", "Upload PDF"])

    if resume_option == "Text":
        resume_content = st.text_area("Enter your resume content:", height=300)
    else:
        resume_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
        if resume_file:
            resume_content = extract_text_from_pdf(resume_file)
            st.success("Resume uploaded successfully!")
        else:
            resume_content = None

    if resume_content:
        st.session_state['resume_content'] = resume_content
        st.success("Resume content saved. Proceed to the 'Tailor Resume' page.")
    else:
        st.warning("Please enter your resume content or upload a PDF.")