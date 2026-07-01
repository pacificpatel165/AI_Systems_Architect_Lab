import streamlit as st
from ui.core.layout import render_layout
from ui.core.app_state import get_system
from ui.documents.document_page import render_document_page

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(page_title="Documents", page_icon="📄", layout="wide")

# ==========================================================
# Initialize
# ==========================================================
system = get_system()

# ==========================================================
# Common Layout
# ==========================================================
render_layout(system)

# ==========================================================
# Documents
# ==========================================================
render_document_page()
