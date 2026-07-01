import streamlit as st
from ui.core.app_state import get_system
from ui.documents.document_browser import render_document_browser
from ui.documents.chunk_viewer import render_chunk_viewer


# ==========================================================
# Documents Page
# ==========================================================
def render_document_page():
    st.title("📄 Documents")
    st.caption("Browse indexed documents and generated chunks.")

    system = get_system()

    chunks = system.chunks
    parent_documents = system.parent_documents

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------
    total_documents = len(parent_documents)
    total_pages = len(
        {(chunk["source_file"], chunk["page_number"]) for chunk in chunks}
    )

    total_chunks = len(chunks)
    col1, col2, col3 = st.columns(3)
    col1.metric("Documents", total_documents)
    col2.metric("Pages", total_pages)
    col3.metric("Chunks", total_chunks)
    st.divider()

    # ------------------------------------------------------
    # Document Explorer
    # ------------------------------------------------------
    render_document_browser(parent_documents, chunks)
    st.divider()

    # ------------------------------------------------------
    # Chunk Viewer
    # ------------------------------------------------------
    render_chunk_viewer(chunks)
