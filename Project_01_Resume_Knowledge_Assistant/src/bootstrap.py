from src.app.resume_assistant import ResumeAssistant
from src.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DEBUG_MODE,
    DOCUMENT_FOLDER,
    EMBEDDING_MODEL_NAME,
    FAISS_INDEX_FILE,
    FAISS_METADATA_FILE,
    LLM_MODEL_NAME,
    RERANKER_MODEL_NAME,
)
from src.embeddings.vector_store import (
    build_faiss_index,
    create_embeddings,
    load_embedding_model,
    load_vector_store,
    save_vector_store,
    vector_store_exists,
)
from src.llm.gemini_client import load_llm
from src.loaders.document_loader import chunk_text_with_metadata, load_documents
from src.logger import get_logger
from src.memory.conversation_memory import conversation_memory
from src.models.model_info import ModelInfo
from src.models.system import SystemState
from src.retrieval.reranker import load_reranker_model

logger = get_logger(__name__)


# ==========================================================
# Initialize System
# ==========================================================
def initialize_system():
    logger.info("Initializing Resume Knowledge Assistant")

    # ------------------------------------------------------
    # Load Documents
    # ------------------------------------------------------
    all_pages_data, parent_documents = load_documents(DOCUMENT_FOLDER)
    logger.info(
        "Loaded %d pages from %d parent documents",
        len(all_pages_data),
        len(parent_documents),
    )

    chunks = chunk_text_with_metadata(all_pages_data, CHUNK_SIZE, CHUNK_OVERLAP)
    logger.info(
        "Created %d chunks using size=%d overlap=%d",
        len(chunks),
        CHUNK_SIZE,
        CHUNK_OVERLAP,
    )

    # ------------------------------------------------------
    # Load Models
    # ------------------------------------------------------
    embedding_model = load_embedding_model(EMBEDDING_MODEL_NAME)
    logger.info("Embedding model loaded: %s", EMBEDDING_MODEL_NAME)
    reranker = load_reranker_model(RERANKER_MODEL_NAME)
    logger.info("Reranker model loaded: %s", RERANKER_MODEL_NAME)
    llm_model = load_llm()
    logger.info("LLM initialized: %s", LLM_MODEL_NAME)

    # ------------------------------------------------------
    # Vector Store
    # ------------------------------------------------------
    if vector_store_exists():
        try:
            logger.info("Loading existing FAISS vector store")
            index, chunks = load_vector_store()
            logger.info("Loaded FAISS index with %d vectors", index.ntotal)
        except Exception:
            logger.exception("Existing FAISS vector store is invalid")
            index, chunks = _build_vector_store(chunks, embedding_model)

    else:
        logger.info("FAISS vector store not found")
        index, chunks = _build_vector_store(chunks, embedding_model)

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
    # System Statistics
    # ------------------------------------------------------
    stats = {
        "pages_loaded": len(all_pages_data),
        "chunks_created": len(chunks),
        "vectors_stored": index.ntotal,
    }

    if DEBUG_MODE:
        logger.debug(
            "System statistics | Pages=%d Chunks=%d Vectors=%d",
            stats["pages_loaded"],
            stats["chunks_created"],
            stats["vectors_stored"],
        )

    # ------------------------------------------------------
    # Model Information
    # ------------------------------------------------------
    model_info = ModelInfo(
        embedding=EMBEDDING_MODEL_NAME, reranker=RERANKER_MODEL_NAME, llm=LLM_MODEL_NAME
    )

    # ------------------------------------------------------
    # System State
    # ------------------------------------------------------
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
    logger.info(
        "System initialized successfully | " "Pages=%d Chunks=%d Vectors=%d",
        stats["pages_loaded"],
        stats["chunks_created"],
        stats["vectors_stored"],
    )
    return system


# ==========================================================
# Build Vector Store
# ==========================================================
def _build_vector_store(chunks, embedding_model):
    logger.info("Building new FAISS vector store")

    embeddings = create_embeddings(chunks, embedding_model)
    index = build_faiss_index(embeddings)
    save_vector_store(index, chunks)
    logger.info("FAISS vector store created | Vectors=%d", index.ntotal)
    logger.debug("FAISS index file: %s", FAISS_INDEX_FILE)
    logger.debug("FAISS metadata file: %s", FAISS_METADATA_FILE)

    return index, chunks
