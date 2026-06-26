from src.config import *
from src.loaders.document_loader import (
    load_documents,
    chunk_text_with_metadata,
)
from src.embeddings.vector_store import (
    load_embedding_model,
    create_embeddings,
    build_faiss_index,
)
from src.retrieval.reranker import (
    load_reranker_model,
)
from src.llm.gemini_client import (
    load_llm,
)
from src.memory.conversation_memory import (
    conversation_memory,
)
from src.app.resume_assistant import (
    ResumeAssistant,
)


# ==========================================================
# Initialize System
# ==========================================================
def initialize_system():
    print()
    print("=" * 80)
    print("INITIALIZING RESUME KNOWLEDGE ASSISTANT")
    print("=" * 80)

    # ------------------------------------------------------
    # Load Documents
    # ------------------------------------------------------
    all_pages_data, parent_documents = load_documents(DOCUMENT_FOLDER)
    chunks = chunk_text_with_metadata(all_pages_data, CHUNK_SIZE, OVERLAP)

    # ------------------------------------------------------
    # Models
    # ------------------------------------------------------
    embedding_model = load_embedding_model(EMBEDDING_MODEL_NAME)
    reranker = load_reranker_model(RERANKER_MODEL_NAME)
    llm_model = load_llm()

    # ------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------
    embeddings = create_embeddings(chunks, embedding_model)

    # ------------------------------------------------------
    # Vector Store
    # ------------------------------------------------------
    index = build_faiss_index(embeddings)
    print("\nSystem Initialized Successfully")

    # ------------------------------------------------------
    # Create Assistant
    # ------------------------------------------------------
    assistant = ResumeAssistant(
        embedding_model=embedding_model,
        reranker=reranker,
        llm_model=llm_model,
        index=index,
        chunks=chunks,
        parent_documents=parent_documents,
        conversation_memory=conversation_memory,
    )

    # ------------------------------------------------------
    # Debug
    # ------------------------------------------------------
    if DEBUG_MODE:
        print()

        print("=" * 80)
        print("SYSTEM STATISTICS")
        print("=" * 80)

        print(f"Pages Loaded     : {len(all_pages_data)}")
        print(f"Chunks Created   : {len(chunks)}")
        print(f"Vectors Stored   : {index.ntotal}")

    return assistant, {
        "pages": len(all_pages_data),
        "chunks": len(chunks),
        "vectors": index.ntotal,
    }
