import platform
import streamlit as st

from src.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_AUTHOR,
    EMBEDDING_MODEL_NAME,
    RERANKER_MODEL_NAME,
    LLM_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
    MAX_MEMORY_TURNS,
    ENABLE_KEYWORD_COMPRESSION,
    ENABLE_SEMANTIC_COMPRESSION,
    USE_LLM,
    DEBUG_MODE,
    EMBEDDING_DIMENSION,
)


# ==========================================================
# Settings Page
# ==========================================================
def render_settings_page():
    st.title("⚙ Settings")
    st.caption("Current system configuration.")

    # ------------------------------------------------------
    # AI Models
    # ------------------------------------------------------
    st.subheader("🤖 AI Models")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Embedding",
        EMBEDDING_MODEL_NAME
    )
    col2.metric(
        "Reranker",
        RERANKER_MODEL_NAME
    )
    col3.metric(
        "LLM",
        LLM_MODEL_NAME
    )
    st.divider()

    # ------------------------------------------------------
    # Document Processing
    # ------------------------------------------------------
    st.subheader("📄 Document Processing")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Chunk Size",
        CHUNK_SIZE
    )
    col2.metric(
        "Chunk Overlap",
        CHUNK_OVERLAP
    )
    col3.metric(
        "Embedding Dimension",
        EMBEDDING_DIMENSION
    )
    st.divider()

    # ------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------
    st.subheader("🔍 Retrieval")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Top K",
        TOP_K
    )
    col2.metric(
        "Memory Turns",
        MAX_MEMORY_TURNS
    )
    col3.metric(
        "LLM Enabled",
        "Yes" if USE_LLM else "No"
    )
    st.success(
        f"✓ Keyword Compression : {'Enabled' if ENABLE_KEYWORD_COMPRESSION else 'Disabled'}"
    )
    st.success(
        f"✓ Semantic Compression : {'Enabled' if ENABLE_SEMANTIC_COMPRESSION else 'Disabled'}"
    )
    st.success("✓ Cross Encoder Reranking")
    st.divider()

    # ------------------------------------------------------
    # System
    # ------------------------------------------------------
    st.subheader("💻 System")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Python",
        platform.python_version()
    )
    col2.metric(
        "Platform",
        platform.system()
    )
    col3.metric(
        "Debug Mode",
        "Enabled" if DEBUG_MODE else "Disabled"
    )
    st.divider()

    # ------------------------------------------------------
    # Project
    # ------------------------------------------------------
    st.subheader("📦 Project")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Project** : {PROJECT_NAME}")
        st.write(f"**Version** : {PROJECT_VERSION}")
    with col2:
        st.write("**Architecture** : RAG Pipeline")
        st.write(f"**Author** : {PROJECT_AUTHOR}")