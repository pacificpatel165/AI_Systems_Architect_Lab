import streamlit as st

# ==========================================================
# Retrieval Inspector
# ==========================================================
import streamlit as st


# ==========================================================
# Retrieval Inspector
# ==========================================================
def render_retrieval_inspector(debug):
    st.header("🔍 Retrieval Inspector")
    retrieval = debug.retrieval.details
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for chunk in retrieval:
        medal = medals.get(chunk["rank"], "🏅")
        title = f"{medal} Rank {chunk['rank']}  |  " f"Chunk #{chunk['chunk_id']}"
        with st.expander(title):
            # ------------------------------------------------------
            # Metrics
            # ------------------------------------------------------
            col1, col2, col3 = st.columns(3)
            col1.metric("Rank", chunk["rank"])
            col2.metric("Chunk ID", chunk["chunk_id"])
            col3.metric("Rerank Score", f"{chunk['rerank_score']:.3f}")

            # ------------------------------------------------------
            # Document Information
            # ------------------------------------------------------
            st.markdown("### 📄 Document Information")
            st.write(f"**File:** {chunk['source_file']}")
            st.write(f"**Page:** {chunk['page_number']}")
            st.write(f"**Document Type:** {chunk['document_type']}")

            # ------------------------------------------------------
            # Retrieved Text
            # ------------------------------------------------------
            st.markdown("### 📑 Retrieved Chunk")
            st.code(chunk["text"], language="text")
