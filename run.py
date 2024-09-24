import os
from dotenv import load_dotenv
import streamlit as st
from app.pages import home, resume_upload, tailor_resume

# Load environment variables
load_dotenv()

# Verify GROQ_API_KEY is loaded
if 'GROQ_API_KEY' in os.environ:
    print("GROQ_API_KEY found in environment variables")
else:
    print("WARNING: GROQ_API_KEY not found in environment variables")

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
        "This app is maintained by [Jithendra Katta]. "
        "Check out our [GitHub](https://github.com/Jithendra-k/resume_tailorizer) page."
    )

if __name__ == "__main__":
    main()