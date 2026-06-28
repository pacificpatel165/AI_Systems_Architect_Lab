import streamlit as st
from ui.components.debug_dashboard import render_debug_dashboard
from ui.components.retrieval_inspector import render_retrieval_inspector
from ui.components.pipeline_visualizer import render_pipeline

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Debug Dashboard",
    page_icon="⚙",
    layout="wide",
)
st.title("⚙ Debug Dashboard")
st.caption("Inspect the Retrieval-Augmented Generation (RAG) pipeline")

# ==========================================================
# No Question Asked Yet
# ==========================================================
if "debug" not in st.session_state:
    st.info("Ask a question from the Resume Assistant first.")
    st.stop()

# ==========================================================
# Render Dashboard
# ==========================================================
with st.container():
    render_pipeline(st.session_state.debug)
st.divider()
with st.container():
    render_debug_dashboard(st.session_state.debug)
st.divider()
with st.container():
    render_retrieval_inspector(st.session_state.debug)
