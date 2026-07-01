import streamlit as st


# ==========================================================
# Document Browser
# ==========================================================
def render_document_browser(parent_documents, chunks):
    st.header("📄 Document Explorer")
    st.caption(f"{len(parent_documents)} parent documents indexed")
    documents = {}

    # ------------------------------------------------------
    # Build Statistics
    # ------------------------------------------------------
    for chunk in chunks:
        filename = chunk["source_file"]
        if filename not in documents:
            documents[filename] = {
                "pages": set(),
                "chunks": 0,
                "type": chunk["document_type"],
                "characters": 0,
                "page_list": [],
            }
        documents[filename]["pages"].add(
            chunk["page_number"]
        )
        documents[filename]["chunks"] += 1

    # ------------------------------------------------------
    # Parent Document Information
    # ------------------------------------------------------
    for parent in parent_documents:
        filename = parent["source_file"]
        if filename not in documents:
            continue
        documents[filename]["characters"] += len(
            parent["text"]
        )
        documents[filename]["page_list"].append(
            {
                "page": parent["page_number"],
                "parent_id": parent["parent_id"],
                "characters": len(parent["text"])
            }
        )

    # ------------------------------------------------------
    # Display
    # ------------------------------------------------------
    for filename, info in sorted(documents.items()):
        with st.expander(f"📄 {filename}"):
            # ----------------------------------------------
            # Summary
            # ----------------------------------------------
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(
                "Pages",
                len(info["pages"])
            )
            col2.metric(
                "Chunks",
                info["chunks"]
            )
            col3.metric(
                "Type",
                info["type"]
            )
            col4.metric(
                "Characters",
                f"{info['characters']:,}"
            )
            st.divider()

            # ----------------------------------------------
            # Pages
            # ----------------------------------------------
            st.markdown("#### 📑 Pages")
            for page in sorted(
                info["page_list"],
                key=lambda x: x["page"]
            ):
                col1, col2, col3 = st.columns([2, 4, 2])
                col1.write(
                    f"**Page {page['page']}**"
                )
                col2.write(
                    f"Parent ID : `{page['parent_id']}`"
                )
                col3.write(
                    f"{page['characters']:,} chars"
                )