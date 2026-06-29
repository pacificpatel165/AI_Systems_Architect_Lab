import platform
import streamlit as st
from src.version import __version__


# ==========================================================
# Sidebar
# ==========================================================
def render_sidebar(system):
    stats = system.stats
    st.sidebar.title("🤖 Resume AI")
    st.sidebar.success("🟢 System Ready")

    # ======================================================
    # Statistics
    # ======================================================
    st.sidebar.divider()
    st.sidebar.markdown("### 📊 Statistics")
    st.sidebar.metric("Pages Loaded", stats["pages_loaded"])
    st.sidebar.metric("Chunks", stats["chunks_created"])
    st.sidebar.metric("Vectors", stats["vectors_stored"])
    st.sidebar.metric("Conversation", len(system.assistant.conversation_memory))

    # ======================================================
    # Models
    # ======================================================
    st.sidebar.divider()
    models = system.model_info
    st.sidebar.markdown("### 🧠 Models")
    st.sidebar.write("**Embedding**")
    st.sidebar.caption(models.embedding)
    st.sidebar.write("**Reranker**")
    st.sidebar.caption(models.reranker)
    st.sidebar.write("**LLM**")
    st.sidebar.caption(models.llm)

    # ======================================================
    # Environment
    # ======================================================
    st.sidebar.divider()
    st.sidebar.markdown("### ⚙ Environment")
    st.sidebar.write(f"**Python**  {platform.python_version()}")
    st.sidebar.write("**Vector DB**  FAISS")
    st.sidebar.write("**Device**  CPU")

    # ======================================================
    # Version
    # ======================================================
    st.sidebar.divider()
    st.sidebar.markdown("### 📦 Version")
    st.sidebar.write("Resume Knowledge Assistant")
    st.sidebar.caption(f"Version {__version__}")
