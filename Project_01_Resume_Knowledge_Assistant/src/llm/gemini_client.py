import time
import google.generativeai as genai
from src.config import GEMINI_API_KEY
from src.logger import get_logger

logger = get_logger(__name__)

# ==========================================================
# Load Gemini
# ==========================================================
def load_llm():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    logger.info("Gemini Loaded: %s", "gemini-2.5-flash")
    return model


# ==========================================================
# Generate Response
# ==========================================================
def generate_response(llm_model, prompt, retries=3):
    for attempt in range(retries):
        try:
            response = llm_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.exception("Error occurred while generating response: %s", str(e))
            time.sleep(5)
            return {"success": False, "answer": "LLM unavailable.", "error": str(e)}
