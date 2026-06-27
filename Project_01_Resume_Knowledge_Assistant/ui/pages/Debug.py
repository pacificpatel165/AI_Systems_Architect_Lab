import streamlit as st
from ui.components.debug_dashboard import render_debug_dashboard

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
render_debug_dashboard(st.session_state.debug)
