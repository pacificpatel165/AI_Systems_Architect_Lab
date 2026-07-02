import streamlit as st
from ui.core.app_state import get_system
from ui.core.layout import render_layout
from ui.about.about_page import render_about_page


# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="About",
    page_icon="ℹ",
    layout="wide",
)

# ==========================================================
# Initialize
# ==========================================================
system = get_system()

# ==========================================================
# Common Layout
# ==========================================================
render_layout(system)

# ==========================================================
# About
# ==========================================================
render_about_page()