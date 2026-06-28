import streamlit as st


# ==========================================================
# Chunk Viewer
# ==========================================================
def render_chunk_viewer(chunks):
    st.header("📑 Chunk Viewer")
    documents = sorted(list({chunk["source_file"] for chunk in chunks}))
    selected_document = st.selectbox("Select Document", documents)

    filtered_chunks = [
        chunk for chunk in chunks if chunk["source_file"] == selected_document
    ]

    for i, chunk in enumerate(filtered_chunks, start=1):
        with st.expander(f"Chunk {i} | Page {chunk['page_number']}"):
            st.write(f"**Document Type:** {chunk['document_type']}")
            st.code(chunk["text"], language="text")
