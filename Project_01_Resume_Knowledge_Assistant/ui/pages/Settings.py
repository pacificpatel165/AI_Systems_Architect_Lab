import streamlit as st
from ui.core.layout import render_layout
from ui.core.app_state import get_system
from ui.settings.settings_page import render_settings_page

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Settings",
    page_icon="⚙",
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
# Settings
# ==========================================================
render_settings_page()
