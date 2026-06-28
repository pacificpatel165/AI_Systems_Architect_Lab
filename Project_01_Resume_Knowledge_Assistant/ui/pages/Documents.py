import streamlit as st
from src.bootstrap import initialize_system
from ui.components.document_browser import render_document_browser
from ui.components.chunk_viewer import render_chunk_viewer

st.set_page_config(page_title="Documents", page_icon="📄", layout="wide")
st.title("📄 Document Explorer")

# ------------------------------------------------------
# Initialize once
# ------------------------------------------------------
if "assistant" not in st.session_state:
    with st.spinner("Initializing System..."):
        assistant, stats = initialize_system()
        st.session_state.assistant = assistant
        st.session_state.stats = stats

# ------------------------------------------------------
# Retrieve data
# ------------------------------------------------------
assistant = st.session_state.assistant
chunks = assistant.chunks
parent_documents = assistant.parent_documents

# ------------------------------------------------------
# UI
# ------------------------------------------------------
render_document_browser(parent_documents, chunks)
st.divider()
render_chunk_viewer(chunks)
