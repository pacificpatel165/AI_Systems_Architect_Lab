from src.config import *
from src.loaders.document_loader import load_documents, chunk_text_with_metadata
from src.embeddings.vector_store import (
    load_embedding_model,
    create_embeddings,
    build_faiss_index,
)
from src.retrieval.reranker import load_reranker_model


# ----------------------------------------
# Load PDFs
# ----------------------------------------
all_pages_data, parent_documents = load_documents(DOCUMENT_FOLDER)

# ----------------------------------------
# Chunking
# ----------------------------------------
chunks = chunk_text_with_metadata(all_pages_data, CHUNK_SIZE, OVERLAP)

# ----------------------------------------
# Models
# ----------------------------------------
embedding_model = load_embedding_model(EMBEDDING_MODEL_NAME)
reranker = load_reranker_model(RERANKER_MODEL_NAME)

# ----------------------------------------
# Embeddings
# ----------------------------------------
embeddings = create_embeddings(chunks, embedding_model)

# ----------------------------------------
# FAISS
# ----------------------------------------
index = build_faiss_index(embeddings)
print("System Initialized")


# ----------------------------------------
# DEBUG MODE
# ----------------------------------------
if DEBUG_MODE:
    print()
    print("=" * 80)
    print("DEBUG MODE ENABLED")
    print("=" * 80)
    print(f"Project Root     : {PROJECT_ROOT}")
    print(f"Data Directory   : {DATA_DIR}")
    print(f"Document Folder  : {DOCUMENT_FOLDER}")
    print(f"FAISS Directory  : {FAISS_DIR}")
    print(f"Memory Directory : {MEMORY_DIR}")
    print(f"Embedding Model  : {EMBEDDING_MODEL_NAME}")
    print(f"Reranker Model   : {RERANKER_MODEL_NAME}")
    print()
    print("=" * 80)
    print("SYSTEM STATISTICS")
    print("=" * 80)
    print(f"Pages Loaded     : {len(all_pages_data)}")
    print(f"Chunks Created   : {len(chunks)}")
    print(f"Vectors Stored   : {index.ntotal}")
    print()
