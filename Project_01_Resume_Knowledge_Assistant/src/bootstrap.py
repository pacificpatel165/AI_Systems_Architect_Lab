from src.config import *
from src.loaders.document_loader import load_documents, chunk_text_with_metadata
from src.embeddings.vector_store import (
    load_embedding_model,
    create_embeddings,
    build_faiss_index,
    load_vector_store,
    save_vector_store,
    vector_store_exists,
)
from src.retrieval.reranker import load_reranker_model
from src.llm.gemini_client import load_llm
from src.memory.conversation_memory import conversation_memory
from src.app.resume_assistant import ResumeAssistant
from src.models.system import SystemState
from src.config import EMBEDDING_MODEL_NAME, RERANKER_MODEL_NAME, LLM_MODEL_NAME
from src.models.model_info import ModelInfo


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
    chunks = chunk_text_with_metadata(all_pages_data, CHUNK_SIZE, CHUNK_OVERLAP)

    # ------------------------------------------------------
    # Models
    # ------------------------------------------------------
    embedding_model = load_embedding_model(EMBEDDING_MODEL_NAME)
    reranker = load_reranker_model(RERANKER_MODEL_NAME)
    llm_model = load_llm()

    # ------------------------------------------------------
    # Vector Store
    # ------------------------------------------------------
    try:
        if vector_store_exists():
            print("Loading Existing Vector Store...")
            index, chunks = load_vector_store()
        else:
            raise FileNotFoundError
    except Exception as e:
        print()
        print("Existing Vector Store Invalid")
        print(e)
        print()
        print("Creating New Vector Store...")
        embeddings = create_embeddings(chunks, embedding_model)
        index = build_faiss_index(embeddings)
        save_vector_store(index, chunks)
        print("=" * 80)
        print("VECTOR STORE CREATED")
        print("=" * 80)

        print(f"Status          : Building New Index")
        print(f"Pages           : {len(all_pages_data)}")
        print(f"Chunks          : {len(chunks)}")
        print(f"Embedding Model : {EMBEDDING_MODEL_NAME}")
        print(f"Saving Cache...")
        print(f"✓ Index File     : {FAISS_INDEX_FILE}")
        print(f"✓ Metadata File  : {FAISS_METADATA_FILE}")

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

    stats = {
        "pages_loaded": len(all_pages_data),
        "chunks_created": len(chunks),
        "vectors_stored": index.ntotal,
    }
    model_info = ModelInfo(
        embedding=EMBEDDING_MODEL_NAME,
        reranker=RERANKER_MODEL_NAME,
        llm=LLM_MODEL_NAME,
    )
    system = SystemState(
        assistant=assistant,
        stats=stats,
        chunks=chunks,
        parent_documents=parent_documents,
        index=index,
        embedding_model=embedding_model,
        reranker=reranker,
        llm_model=llm_model,
        model_info=model_info,
    )
    return system
