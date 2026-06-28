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
        st.write(f"**Type:** {debug.query.query_type}")
        st.write(f"**Question:** {debug.query.question}")
        st.write(f"**Rewritten:** {debug.query.rewritten_query}")

    # ------------------------------------------------------
    # Strategy
    # ------------------------------------------------------
    with st.expander("🎯 Strategy"):
        strategy = debug.query.strategy
        status(strategy.rewrite, "Query Rewrite")
        status(strategy.metadata, "Metadata Filter")
        status(strategy.parent, "Parent Retrieval")
        status(strategy.compression, "Context Compression")

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------
    with st.expander("📂 Metadata"):
        st.write(debug.query.document_filter)

    # ------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------
    with st.expander("🔍 Retrieval"):
        st.write(f"Retrieved : {len(debug.retrieval.retrieved_indices)}")
        st.write(f"Top Chunks : {debug.retrieval.top_indices}")

    # ------------------------------------------------------
    # Parent Retrieval
    # ------------------------------------------------------
    with st.expander("📄 Parent Retrieval"):
        st.write(debug.retrieval.parent_ids)

    # ------------------------------------------------------
    # Compression
    # ------------------------------------------------------
    with st.expander("🗜 Context Compression", expanded=True):
        col1, col2, col3 = st.columns(3)
        col1.metric("Original", debug.context.original_length)
        col2.metric("Compressed", debug.context.compressed_length)
        col3.metric("Saved %", f"{debug.context.compression_ratio:.1f}%")

    # ------------------------------------------------------
    # Memory
    # ------------------------------------------------------
    with st.expander("🧠 Memory"):
        st.metric("Conversation Turns", debug.memory.turns)
    
    # ------------------------------------------------------
    # Performance
    # ------------------------------------------------------
    with st.expander("⚡ Performance", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Conversation Turns", debug.memory.turns)
        col2.metric("Retrieved Chunks", debug.performance.retrieved_chunks)
        col3.metric("Returned Chunks", debug.performance.returned_chunks)
        col4.metric("Latency", f"{debug.performance.latency:.3f} s")
