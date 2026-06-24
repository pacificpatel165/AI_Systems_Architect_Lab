from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import numpy as np

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
    print(f"Vectors Stored : " f"{index.ntotal}")
    return index
