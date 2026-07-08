import time
from google import genai

from src.config import GEMINI_API_KEY, LLM_MODEL_NAME
from src.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# Load Gemini
# ==========================================================
def load_llm():
    logger.info("Initializing Gemini client: %s", LLM_MODEL_NAME)
    client = genai.Client(api_key=GEMINI_API_KEY)
    logger.info("Gemini client initialized: %s", LLM_MODEL_NAME)
    return client


# ==========================================================
# Generate Response
# ==========================================================
def generate_response(llm_model, prompt, retries=3):
    for attempt in range(1, retries + 1):
        try:
            logger.debug("Generating Gemini response. Attempt %d/%d", attempt, retries)
            response = llm_model.models.generate_content(
                model=LLM_MODEL_NAME, contents=prompt
            )
            logger.info("Gemini response generated successfully")
            return response.text
        except Exception as error:
            logger.exception(
                "Gemini generation failed. Attempt %d/%d: %s",
                attempt,
                retries,
                str(error),
            )
            if attempt < retries:
                logger.warning("Retrying Gemini request in 5 seconds")
                time.sleep(5)
    logger.error("Gemini unavailable after %d attempts", retries)
    return "LLM unavailable."
