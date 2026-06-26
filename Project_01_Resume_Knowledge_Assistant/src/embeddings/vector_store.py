from operator import index

from sentence_transformers import SentenceTransformer, CrossEncoder
import pickle
from pathlib import Path
import faiss
import numpy as np

from src.config import (
    FAISS_INDEX_FILE,
    FAISS_METADATA_FILE,
)


# ==========================================================
# Models
# ==========================================================
def load_embedding_model(model_name):
    model = SentenceTransformer(model_name)
    print("Embedding Model Loaded")
    return model


# ==========================================================
# Embeddings
# ==========================================================
def create_embeddings(chunks, embedding_model):
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.encode(chunk_texts, show_progress_bar=True)
    return embeddings


# ==========================================================
# FAISS
# ==========================================================
def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    print(f"Vectors Created : " f"{index.ntotal}")
    return index


# ==========================================================
# Save Vector Store
# ==========================================================
def save_vector_store(index, chunks):
    faiss.write_index(index, str(FAISS_INDEX_FILE))
    with open(FAISS_METADATA_FILE, "wb") as file:
        pickle.dump(chunks, file)
    print(f"Vectors Saved : {index.ntotal}")


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
    print(f"Status         : Loaded from Cache")
    print(f"Index File     : {FAISS_INDEX_FILE}")
    print(f"Metadata File  : {FAISS_METADATA_FILE}")
    print(f"Vectors Loaded : {index.ntotal}")
    print(f"Chunks Loaded  : {len(chunks)}")
    return (index, chunks)


# ==========================================================
# Check Vector Store
# ==========================================================
def vector_store_exists():
    return FAISS_INDEX_FILE.exists() and FAISS_METADATA_FILE.exists()
