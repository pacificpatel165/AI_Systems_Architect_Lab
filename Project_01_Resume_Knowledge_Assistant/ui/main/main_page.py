import streamlit as st
from ui.core.footer import render_footer


# ==========================================================
# Main Page
# ==========================================================
def render_main_page(system):
    st.subheader("🏠 Main")
    st.info(
        "Main page refactoring is in progress.\n\n"
        "Next we will add:\n"
        "- Quick Questions\n"
        "- Chat Toolbar\n"
        "- Chat History\n"
        "- Chat Input"
    )
    render_footer()
