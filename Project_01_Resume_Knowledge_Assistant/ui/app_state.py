import streamlit as st
from src.bootstrap import initialize_system


# ==========================================================
# Get System
# ==========================================================
@st.cache_resource(show_spinner=False)
def load_system():
    return initialize_system()


def get_system():
    return load_system()
