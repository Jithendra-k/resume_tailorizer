# Resume Tailorizer

Resume Tailorizer is an AI-powered application that helps job seekers tailor their resumes to specific job descriptions. By analyzing job postings and the user's existing resume, it generates a customized resume that highlights relevant skills and experiences.

## Features

- Job description scraping from provided URLs
- Resume parsing from text or PDF upload
- AI-powered resume tailoring using LLM technology
- PDF generation of tailored resumes
- User-friendly web interface built with Streamlit

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/resume-tailorizer.git
   cd resume-tailorizer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app/main.py
   ```

2. Open your web browser and go to `http://localhost:8501`

3. Follow the on-screen instructions to upload your resume and provide a job posting URL.

4. Review the tailored resume and download the PDF version.

## Project Structure

```
resume_tailorizer/
│
├── app/
│   ├── main.py
│   ├── pages/
│   ├── components/
│   └── utils/
│
├── data/
├── models/
├── tests/
├── config/
├── requirements.txt
├── README.md
└── .gitignore
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the web application framework
- [LangChain](https://github.com/hwchase17/langchain) for LLM integration
- [ChromaDB](https://github.com/chroma-core/chroma) for vector storage
- [Groq](https://groq.com/) for the LLM API