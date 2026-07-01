import streamlit as st
from ui.debug.pipeline_visualizer import render_pipeline
from ui.debug.debug_dashboard import render_debug_dashboard
from ui.debug.retrieval_inspector import render_retrieval_inspector


# ==========================================================
# Debug Page
# ==========================================================
def render_debug_page():
    st.title("⚙ Debug Dashboard")
    st.caption("Inspect the Retrieval-Augmented Generation (RAG) pipeline")

    # ------------------------------------------------------
    # No Question Asked Yet
    # ------------------------------------------------------
    if "debug" not in st.session_state or st.session_state.debug is None:
        st.info("Ask a question from the Resume Assistant first.")
        return

    debug = st.session_state.debug
    render_pipeline(debug)
    st.divider()
    render_debug_dashboard(debug)
    st.divider()
    render_retrieval_inspector(debug)
