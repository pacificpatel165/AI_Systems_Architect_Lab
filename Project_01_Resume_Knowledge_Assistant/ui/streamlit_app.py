import streamlit as st
from ui.core.app_state import get_system
from ui.core.layout import render_layout
from ui.main.main_page import render_main_page

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Resume Knowledge Assistant", page_icon="🤖", layout="wide"
)


# ==========================================================
# Initialize System
# ==========================================================
system = get_system()


# ==========================================================
# Render Application
# ==========================================================
render_layout(system)
render_main_page(system)
