import streamlit as st


# ==========================================================
# Pipeline Visualizer
# ==========================================================
def render_pipeline(debug):
    st.header("🚀 Pipeline Visualizer")
    strategy = debug.query.strategy
    stages = [
        ("🧠 Question", True, debug.query.question),
        ("🏷 Query Classification", True, debug.query.query_type),
        ("✏ Query Rewriting", strategy.rewrite, debug.query.rewritten_query),
        (
            "🔍 Hybrid Retrieval",
            True,
            f"{debug.performance.retrieved_chunks} chunks retrieved",
        ),
        (
            "📂 Metadata Filter",
            strategy.metadata,
            debug.query.document_filter if debug.query.document_filter else "No filter",
        ),
        ("⭐ Reranker", True, f"{debug.performance.returned_chunks} chunks selected"),
        (
            "📄 Parent Retrieval",
            strategy.parent,
            f"{len(debug.retrieval.parent_ids)} parent documents",
        ),
        (
            "🗜 Context Compression",
            strategy.compression,
            f"{debug.context.compression_ratio:.1f}% reduction",
        ),
        ("💬 Conversation Memory", True, f"{debug.memory.turns} turns"),
        ("🤖 Gemini", True, "Prompt Generated"),
    ]

    for title, enabled, value in stages:
        icon = "🟢" if enabled else "⚪"
        with st.expander(f"{icon} {title}"):
            st.write(value)
