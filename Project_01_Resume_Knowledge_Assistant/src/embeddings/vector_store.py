from sentence_transformers import SentenceTransformer
import pickle
import faiss
import numpy as np
from src.config import FAISS_INDEX_FILE, FAISS_METADATA_FILE
from src.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# Models
# ==========================================================
def load_embedding_model(model_name):
    model = SentenceTransformer(model_name)
    logger.info("Loading embedding model: %s", model_name)
    return model


# ==========================================================
# Embeddings
# ==========================================================
def create_embeddings(chunks, embedding_model):
    chunk_texts = [chunk["text"] for chunk in chunks]
    logger.info("Generating embeddings for %d chunks", len(chunks))
    embeddings = embedding_model.encode(chunk_texts, show_progress_bar=True)
    logger.info("Embedding generation complete")
    return embeddings


# ==========================================================
# FAISS
# ==========================================================
def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    logger.info("FAISS index created with %d vectors", index.ntotal)
    return index


# ==========================================================
# Save Vector Store
# ==========================================================
def save_vector_store(index, chunks):
    faiss.write_index(index, str(FAISS_INDEX_FILE))
    with open(FAISS_METADATA_FILE, "wb") as file:
        pickle.dump(chunks, file)
    logger.info("Vector store[%d] saved successfully", index.ntotal)


# ==========================================================
# Load Vector Store
# ==========================================================
def load_vector_store():
    index = faiss.read_index(str(FAISS_INDEX_FILE))
    with open(FAISS_METADATA_FILE, "rb") as file:
        chunks = pickle.load(file)
    print("=" * 80)
    print("VECTOR STORE LOADED")
    print("=" * 80)
    logger.info("Status         : Loaded from Cache")
    logger.info("Index File     : %s", FAISS_INDEX_FILE)
    logger.info("Metadata File  : %s", FAISS_METADATA_FILE)
    logger.info("Vectors Loaded : %d", index.ntotal)
    logger.info("Chunks Loaded  : %d", len(chunks))
    logger.info("Loaded vector store (%d vectors)", index.ntotal)
    return (index, chunks)


# ==========================================================
# Check Vector Store
# ==========================================================
def vector_store_exists():
    return FAISS_INDEX_FILE.exists() and FAISS_METADATA_FILE.exists()
