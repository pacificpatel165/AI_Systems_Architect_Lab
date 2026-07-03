import time
import google.generativeai as genai
from src.config import GEMINI_API_KEY


# ==========================================================
# Load Gemini
# ==========================================================
def load_llm():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    print("Gemini Loaded")
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
            print(f"Retry {attempt+1}")
            print(e)
            time.sleep(5)
            return {"success": False, "answer": "LLM unavailable.", "error": str(e)}
