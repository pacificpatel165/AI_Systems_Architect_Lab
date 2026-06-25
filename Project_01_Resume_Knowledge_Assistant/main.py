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
from src.rewriting.query_rewriter import rewrite_query, print_rewrite_debug
from src.memory.conversation_memory import conversation_memory, save_to_memory
from src.retrieval.metadata_filter import (
    get_document_filter,
    filter_retrieved_results,
    print_metadata_filter,
)
from src.memory.conversation_memory import (
    conversation_memory,
    build_memory_context,
    save_to_memory,
    print_memory_stats,
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
# TEST 1 : Hybrid Retrieval
# ==========================================================
def test_hybrid_retrieval():
    inspect_retrieval("Which projects used Python?", embedding_model, index, chunks)


# ==========================================================
# TEST 2 : Metadata Filtering
# ==========================================================
def test_metadata_filter():
    question = "Which AWS certifications do I have?"
    document_type = get_document_filter(question)
    print_metadata_filter(question, document_type)


# ==========================================================
# TEST 3 : Reranking
# ==========================================================
def test_reranking():
    question = "Which projects used Python?"
    retrieved_indices = hybrid_search(
        question, embedding_model, index, chunks, semantic_k=10, final_k=10
    )
    ranked_results = rerank_results(question, retrieved_indices, chunks, reranker)
    print_reranked_results(ranked_results)
    top_chunks = get_top_reranked(ranked_results)
    print()
    print("TOP CHUNKS")
    print(top_chunks)


# ==========================================================
# TEST 4 : Conversation Memory
# ==========================================================
def test_memory():
    conversation_memory.clear()
    save_to_memory(
        question="Which projects used Python?",
        answer="PMA and TA5K",
        top_indices=[0, 1, 2],
        chunks=chunks,
        conversation_memory=conversation_memory,
    )
    save_to_memory(
        question="Which company was that for?",
        answer="Adtran",
        top_indices=[0, 1, 2],
        chunks=chunks,
        conversation_memory=conversation_memory,
    )
    print(build_memory_context(conversation_memory))
    print_memory_stats(conversation_memory)


# ==========================================================
# TEST 5 : Query Rewriting
# ==========================================================
def test_query_rewriting():
    conversation_memory.clear()
    question = "Which projects used Python?"
    retrieved = hybrid_search(question, embedding_model, index, chunks)
    save_to_memory(question, "PMA and TA5K", retrieved[:3], chunks, conversation_memory)
    followup = "Which company was that for?"
    rewritten = rewrite_query(followup, conversation_memory)
    print_rewrite_debug(followup, rewritten)
    inspect_retrieval(rewritten, embedding_model, index, chunks)


# ==========================================================
# TEST MODE
# ==========================================================
TEST_MODE = "rewrite"

if TEST_MODE == "retrieval":
    test_hybrid_retrieval()
elif TEST_MODE == "metadata":
    test_metadata_filter()
elif TEST_MODE == "reranker":
    test_reranking()
elif TEST_MODE == "memory":
    test_memory()
elif TEST_MODE == "rewrite":
    test_query_rewriting()
elif TEST_MODE == "all":
    test_hybrid_retrieval()
    test_metadata_filter()
    test_reranking()
    test_memory()
    test_query_rewriting()

if __name__ == "__main__":
    pass
