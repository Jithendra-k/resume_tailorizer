import os
from langchain.llms import Groq, Ollama
from langchain.callbacks import get_openai_callback

class LLMService:
    def __init__(self):
        self.groq_llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.ollama_llm = Ollama(model="llama2")
        self.daily_token_limit = 20000
        self.token_count = 0

    def process(self, prompt):
        if self.token_count < self.daily_token_limit:
            with get_openai_callback() as cb:
                response = self.groq_llm(prompt)
                self.token_count += cb.total_tokens
            return response
        else:
            return self.ollama_llm(prompt)

    def reset_token_count(self):
        self.token_count = 0  # Call this method daily to reset the count

llm_service = LLMService()

def generate_tailored_resume(job_description, resume_content):
    prompt = f"""
    Given the following job description and resume content, 
    create a tailored resume that highlights relevant skills and experiences:

    Job Description:
    {job_description}

    Resume Content:
    {resume_content}

    Provide the tailored resume content:
    """
    return llm_service.process(prompt)