import streamlit as st


# ==========================================================
# Document Browser
# ==========================================================
def render_document_browser(parent_documents, chunks):
    st.header("📄 Document Explorer")
    documents = {}

    # ------------------------------------------------------
    # Build document statistics
    # ------------------------------------------------------
    for chunk in chunks:
        filename = chunk["source_file"]
        if filename not in documents:
            documents[filename] = {
                "pages": set(),
                "chunks": 0,
                "type": chunk["document_type"],
            }

        documents[filename]["pages"].add(chunk["page_number"])
        documents[filename]["chunks"] += 1

    # ------------------------------------------------------
    # Display cards
    # ------------------------------------------------------
    for filename, info in sorted(documents.items()):
        with st.expander(f"📄 {filename}", expanded=False):
            col1, col2, col3 = st.columns(3)
            col1.metric("Pages", len(info["pages"]))
            col2.metric("Chunks", info["chunks"])
            col3.metric("Type", info["type"])
