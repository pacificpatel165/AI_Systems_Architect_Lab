import streamlit as st


# ==========================================================
# Chunk Viewer
# ==========================================================
def render_chunk_viewer(chunks):
    st.header("📑 Chunk Viewer")

    # ------------------------------------------------------
    # No Chunks
    # ------------------------------------------------------
    if not chunks:
        st.info("No chunks available.")
        return

    # ------------------------------------------------------
    # Document Selection
    # ------------------------------------------------------
    documents = sorted({chunk["source_file"] for chunk in chunks})
    selected_document = st.selectbox("Select Document", documents)

    # ------------------------------------------------------
    # Filter Chunks
    # ------------------------------------------------------
    filtered_chunks = [
        chunk for chunk in chunks if chunk["source_file"] == selected_document
    ]
    st.caption(f"{len(filtered_chunks)} chunks available")

    # ------------------------------------------------------
    # Display Chunks
    # ------------------------------------------------------
    st.metric(
        "Average Chunk Size",
        f"{sum(len(c['text']) for c in filtered_chunks) // len(filtered_chunks)} chars",
    )
    for index, chunk in enumerate(
        filtered_chunks,
        start=1,
    ):
        # Parent ID may not exist in older datasets
        parent_id = chunk.get("parent_id", "N/A")
        title = (
            f"Chunk {index}" f" | Page {chunk['page_number']}" f" | Parent {parent_id}"
        )
        with st.expander(title):
            # ----------------------------------------------
            # Metadata
            # ----------------------------------------------
            col1, col2, col3 = st.columns(3)
            col1.metric("Page", chunk["page_number"])
            col2.metric("Parent", parent_id)
            col3.metric("Characters", len(chunk["text"]))
            st.write(f"**Document Type:** {chunk['document_type']}")
            st.write(f"**Source File:** {chunk['source_file']}")

            # ----------------------------------------------
            # Chunk Text
            # ----------------------------------------------
            st.markdown("#### 📄 Chunk Text")
            st.code(chunk["text"], language="text")
