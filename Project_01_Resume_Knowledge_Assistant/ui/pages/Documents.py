import streamlit as st
from src.bootstrap import initialize_system
from ui.components.document_browser import render_document_browser
from ui.components.chunk_viewer import render_chunk_viewer
from ui.app_state import get_system

st.set_page_config(page_title="Documents", page_icon="📄", layout="wide")
st.title("📄 Document Explorer")

# ------------------------------------------------------
# Initialize once
# ------------------------------------------------------
if "assistant" not in st.session_state:
    with st.spinner("Initializing System..."):
        system = get_system()
        st.session_state.system = system

# ------------------------------------------------------
# Retrieve data
# ------------------------------------------------------
assistant = st.session_state.system.assistant
chunks = assistant.chunks
parent_documents = st.session_state.system.parent_documents

# ------------------------------------------------------
# UI
# ------------------------------------------------------
render_document_browser(parent_documents, chunks)
st.divider()
render_chunk_viewer(chunks)
