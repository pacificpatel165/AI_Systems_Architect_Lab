from pathlib import Path
import streamlit as st


# ==========================================================
# Load CSS Theme
# ==========================================================
def load_css():
    css_file = Path(__file__).parent.parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file, encoding="utf-8") as file:
            st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)
