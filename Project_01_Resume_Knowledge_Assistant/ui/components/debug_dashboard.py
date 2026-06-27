import streamlit as st
from ui.components.debug_widgets import status


# ==========================================================
# Debug Dashboard
# ==========================================================
def render_debug_dashboard(debug):
    st.divider()
    st.header("⚙ Debug Dashboard")

    # ------------------------------------------------------
    # Query
    # ------------------------------------------------------
    with st.expander("🧠 Query"):
        st.write(f"**Type:** {debug['query_type']}")
        st.write(f"**Question:** {debug['question']}")
        st.write(f"**Rewritten:** {debug['rewritten_query']}")

    # ------------------------------------------------------
    # Strategy
    # ------------------------------------------------------
    with st.expander("🎯 Strategy"):
        strategy = debug["strategy"]
        status(strategy["rewrite"], "Query Rewrite")
        status(strategy["metadata"], "Metadata Filter")
        status(strategy["parent"], "Parent Retrieval")
        status(strategy["compression"], "Context Compression")

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------
    with st.expander("📂 Metadata"):
        st.write(debug["document_filter"])

    # ------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------
    with st.expander("🔍 Retrieval"):
        st.write(f"Retrieved : {len(debug['retrieved_indices'])}")
        st.write(f"Top Chunks : {debug['top_indices']}")

    # ------------------------------------------------------
    # Parent Retrieval
    # ------------------------------------------------------
    with st.expander("📄 Parent Retrieval"):
        st.write(debug["parent_ids"])

    # ------------------------------------------------------
    # Compression
    # ------------------------------------------------------
    with st.expander("🗜 Context Compression", expanded=True):
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Original",
            debug["original_length"],
        )
        col2.metric(
            "Compressed",
            debug["compressed_length"],
        )
        col3.metric("Saved %", f"{debug['compression_ratio']:.1f}%")

    # ------------------------------------------------------
    # Memory
    # ------------------------------------------------------
    with st.expander("🧠 Memory"):
        st.metric(
            "Conversation Turns",
            debug["memory_size"],
        )

    # ------------------------------------------------------
    # Perfromance
    # ------------------------------------------------------
    with st.expander("⚡ Performance", expanded=True):
        col1, col2 = st.columns(2)
        col1.metric(
            "Conversation Turns",
            debug["memory_size"],
        )
        col2.metric(
            "Retrieved Chunks",
            len(debug["retrieved_indices"]),
        )
