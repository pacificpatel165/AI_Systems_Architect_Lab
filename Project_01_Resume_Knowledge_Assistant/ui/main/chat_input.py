import streamlit as st


# ==========================================================
# Chat Input
# ==========================================================
def render_chat_input():
    """
    Returns either:

        • Typed question
        • Suggested question selected from popup
    """
    typed_question = st.chat_input("Ask anything about your resume...")
    suggested_question = st.session_state.pop("selected_question", None)
    return typed_question or suggested_question
