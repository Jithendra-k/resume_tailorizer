import os
import streamlit as st
from dotenv import load_dotenv
from pages import home, resume_upload, tailor_resume

# Load environment variables
load_dotenv()

# Access environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
LLM_PROVIDER = os.getenv("LLM_PROVIDER")
LLM_MODEL = os.getenv("LLM_MODEL")

st.set_page_config(page_title="Resume Tailorizer", layout="wide")

# Create a dictionary of pages
PAGES = {
    "Home": home,
    "Upload Resume": resume_upload,
    "Tailor Resume": tailor_resume
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Display the selected page
    page = PAGES[selection]
    page.show()

    # Add a footer
    st.sidebar.markdown("---")
    st.sidebar.info(
        "This app is maintained by [Your Name/Company]. "
        "Check out our [GitHub](https://github.com/yourusername/resume-tailorizer) page."
    )

if __name__ == "__main__":
    main()