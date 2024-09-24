import os
from dotenv import load_dotenv
import logging
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Access environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class LLMService:
    def __init__(self):
        self.groq_llm = None
        self.ollama_llm = None
        self.daily_token_limit = 20000
        self.token_count = 0

        #logger.info("groq api key: ", GROQ_API_KEY)
        if GROQ_API_KEY:
            try:
                self.groq_llm = ChatGroq(
                    model="mixtral-8x7b-32768",
                    temperature=0,
                    max_tokens=None,
                    groq_api_key=GROQ_API_KEY
                )
                logger.info("Groq LLM (ChatGroq) initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq LLM: {str(e)}")
        else:
            logger.warning("GROQ_API_KEY not found in environment variables")

        # Initialize Ollama
        try:
            self.ollama_llm = ChatOllama(model="llama2")
            logger.info("Ollama LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {str(e)}")

    def process(self, prompt):
        #logger.info("token count = ",self.token_count, "Daily token: ",self.daily_token_limit)
        logger.info(self.groq_llm)
        if self.groq_llm and self.token_count < self.daily_token_limit:
            try:
                logger.info("Attempting to use Groq LLM")
                messages = [
                    SystemMessage(
                        content="You are a helpful assistant that tailors resumes based on job descriptions."),
                    HumanMessage(content=prompt)
                ]
                response = self.groq_llm.invoke(messages)
                self.token_count += len(response.content.split())  # Rough estimation
                logger.info("Successfully used Groq LLM")
                return response.content
            except Exception as e:
                logger.error(f"Error using Groq: {str(e)}")
        else:
            if not self.groq_llm:
                logger.info("Groq LLM not available")
            elif self.token_count >= self.daily_token_limit:
                logger.info("Groq daily token limit reached")

        if self.ollama_llm:
            try:
                logger.info("Attempting to use Ollama LLM")
                messages = [
                    SystemMessage(
                        content="You are a helpful assistant that tailors resumes based on job descriptions."),
                    HumanMessage(content=prompt)
                ]
                response = self.ollama_llm.invoke(messages)
                logger.info("Successfully used Ollama LLM")
                return response.content
            except Exception as e:
                logger.error(f"Error using Ollama: {str(e)}")

        logger.error("All LLM options failed")
        return "I'm sorry, but I'm currently unable to process your request due to technical difficulties. Please try again later or contact support."

    def reset_token_count(self):
        self.token_count = 0
        logger.info("Token count reset")


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