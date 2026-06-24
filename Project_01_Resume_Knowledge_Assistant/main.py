from src.config import *
from src.loaders.document_loader import load_documents, chunk_text_with_metadata
from src.embeddings.vector_store import (
    load_embedding_model,
    create_embeddings,
    build_faiss_index,
)
from src.retrieval.reranker import (
    load_reranker_model,
    rerank_results,
    get_top_reranked,
    print_reranked_results,
)

from src.retrieval.retriever import hybrid_search, inspect_retrieval
from src.retrieval.metadata_filter import (
    get_document_filter,
    filter_retrieved_results,
    print_metadata_filter,
)

# ==========================================================
# STEP 1 : Load Documents
# ==========================================================
all_pages_data, parent_documents = load_documents(DOCUMENT_FOLDER)


# ==========================================================
# STEP 2 : Create Chunks
# ==========================================================
chunks = chunk_text_with_metadata(all_pages_data, CHUNK_SIZE, OVERLAP)


# ==========================================================
# STEP 3 : Load AI Models
# ==========================================================
embedding_model = load_embedding_model(EMBEDDING_MODEL_NAME)
reranker = load_reranker_model(RERANKER_MODEL_NAME)


# ==========================================================
# STEP 4 : Generate Embeddings
# ==========================================================
embeddings = create_embeddings(chunks, embedding_model)


# ==========================================================
# STEP 5 : Build FAISS Index
# ==========================================================
index = build_faiss_index(embeddings)
print("System Initialized")


# ==========================================================
# STEP 6 : Debug Information
# ==========================================================
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

    print()

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


# ==========================================================
# STEP 7 : Retrieval Testing
# ==========================================================
inspect_retrieval("Which projects used Python?", embedding_model, index, chunks)


# ==========================================================
# STEP 8 : Quick Metadata Filter Testing
# ==========================================================
question = "Which AWS certifications do I have?"
document_type = get_document_filter(question)
print_metadata_filter(question, document_type)

# ==========================================================
# STEP 9 : Reranking Testing
# ==========================================================
question = "Which projects used Python?"
retrieved_indices = hybrid_search(
    question, embedding_model, index, chunks, semantic_k=10, final_k=10
)

ranked_results = rerank_results(question, retrieved_indices, chunks, reranker)
print_reranked_results(ranked_results)
top_chunks = get_top_reranked(ranked_results, top_n=3)

print()
print("TOP CHUNKS")
print(top_chunks)


if __name__ == "__main__":
    pass
