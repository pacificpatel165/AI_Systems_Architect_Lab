import streamlit as st
from src.version import __version__

# ==========================================================
# Sidebar
# ==========================================================
def render_sidebar(system):
    stats = system.stats
    st.sidebar.title("🤖 Resume AI")
    st.sidebar.success("🟢 System Ready")
    st.sidebar.divider()
    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------
    st.sidebar.subheader("📊 Statistics")
    st.sidebar.metric("Pages Loaded", stats["pages_loaded"])
    st.sidebar.metric("Chunks", stats["chunks_created"])
    st.sidebar.metric("Vectors", stats["vectors_stored"])
    st.sidebar.metric("Conversation", len(system.assistant.conversation_memory))
    st.sidebar.divider()

    # ------------------------------------------------------
    # Models
    # ------------------------------------------------------
    st.sidebar.subheader("🧠 Models")
    st.sidebar.write("**Embedding**")
    st.sidebar.caption("all-MiniLM-L6-v2")
    st.sidebar.write("**Reranker**")
    st.sidebar.caption("cross-encoder")
    st.sidebar.write("**LLM**")
    st.sidebar.caption("Gemini 2.5 Flash")
    st.sidebar.divider()

    # ------------------------------------------------------
    # Version
    # ------------------------------------------------------
    st.sidebar.caption(f"Version {__version__}")
