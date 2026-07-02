import streamlit as st
from src.config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_AUTHOR,
    EMBEDDING_MODEL_NAME,
    RERANKER_MODEL_NAME,
    LLM_MODEL_NAME,
)


# ==========================================================
# About Page
# ==========================================================
def render_about_page():
    st.title("ℹ About")
    st.caption("Project overview and architecture.")

    # ------------------------------------------------------
    # Project
    # ------------------------------------------------------
    st.subheader("🤖 Resume Knowledge Assistant")
    st.write("""
This project demonstrates a **Retrieval-Augmented Generation (RAG)** pipeline
for answering questions about resumes, certifications, project notes and
technical documents.

The goal of this project is to understand the complete lifecycle of a
production-ready RAG application while following clean software architecture.
""")
    st.divider()

    # ------------------------------------------------------
    # Architecture
    # ------------------------------------------------------
    st.subheader("🏗 Architecture")
    st.code("""
                    PDF Documents
                    │
                    ▼
                    Document Loader
                    │
                    ▼
                    Parent Documents
                    │
                    ▼
                    Chunking
                    │
                    ▼
                    Embeddings
                    │
                    ▼
                    FAISS Vector Database
                    │
                    ▼
                    Retriever
                    │
                    ▼
                    Cross Encoder Reranker
                    │
                    ▼
                    Context Compression
                    │
                    ▼
                    Gemini LLM
                    │
                    ▼
                    Final Answer
    """, language="text",)
    st.divider()

    # ------------------------------------------------------
    # AI Models
    # ------------------------------------------------------
    st.subheader("🤖 AI Models")
    col1, col2, col3 = st.columns(3)
    col1.metric("Embedding", EMBEDDING_MODEL_NAME)
    col2.metric("Reranker", RERANKER_MODEL_NAME)
    col3.metric("LLM", LLM_MODEL_NAME)
    st.divider()

    # ------------------------------------------------------
    # Technologies
    # ------------------------------------------------------
    st.subheader("📚 Technologies")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
- Python
- Streamlit
- FAISS
- NumPy
- PyPDF
""")
    with col2:
        st.markdown("""
- Sentence Transformers
- Cross Encoder
- Google Gemini
- dotenv
- Git / GitHub
""")
    st.divider()
    # ------------------------------------------------------
    # Project Structure
    # ------------------------------------------------------
    st.subheader("📂 Project Structure")
    st.code(
        """
src/
├── app/
├── config/
├── data/
├── models/
├── retrieval/
├── utils/

ui/
├── core/
├── main/
├── debug/
├── documents/
├── settings/
├── about/
├── pages/

tests/
""",
        language="text",
    )
    st.divider()
    # ------------------------------------------------------
    # Learning Objectives
    # ------------------------------------------------------
    st.subheader("🎯 Learning Objectives")
    st.markdown("""
✅ Retrieval-Augmented Generation (RAG)

✅ Vector Databases (FAISS)

✅ Semantic Search

✅ Cross Encoder Reranking

✅ Parent Retrieval

✅ Context Compression

✅ Streamlit Dashboard

✅ Clean Project Architecture

✅ Python Best Practices
""")
    st.divider()
    # ------------------------------------------------------
    # Future Roadmap
    # ------------------------------------------------------
    st.subheader("🚀 Future Roadmap")
    st.markdown("""
- Hybrid Search (Vector + BM25)
- Multi-document RAG
- RAG Evaluation
- Prompt Engineering
- Semantic Cache
- Conversation Memory
- AI Agents
- Model Context Protocol (MCP)
- Production Deployment
""")
    st.divider()

    # ------------------------------------------------------
    # Author
    # ------------------------------------------------------
    st.subheader("👨‍💻 Project Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Project** : {PROJECT_NAME}")
        st.write(f"**Version** : {PROJECT_VERSION}")
    with col2:
        st.write(f"**Author** : {PROJECT_AUTHOR}")
        st.write("**Architecture** : RAG Pipeline")
