# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENT_FOLDER = DATA_DIR / "documents"
FAISS_DIR = DATA_DIR / "faiss"
MEMORY_DIR = DATA_DIR / "memory"

# ----------------------------------------------------------
# Gemini
# ----------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL_NAME = "gemini-2.5-flash"
USE_LLM = False

# ----------------------------------------------------------
# RAG Settings
# ----------------------------------------------------------
DEBUG_MODE = True
CHUNK_SIZE = 800
OVERLAP = 200
TOP_K = 5
MAX_MEMORY_TURNS = 5

# ----------------------------------------------------------
# Compression Settings
# ----------------------------------------------------------
ENABLE_KEYWORD_COMPRESSION = True
ENABLE_SEMANTIC_COMPRESSION = True

# ----------------------------------------------------------
# Models
# ----------------------------------------------------------
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ----------------------------------------------------------
# FAISS Storage
# ----------------------------------------------------------
FAISS_INDEX_FILE = FAISS_DIR / "index.faiss"
FAISS_METADATA_FILE = FAISS_DIR / "metadata.pkl"
