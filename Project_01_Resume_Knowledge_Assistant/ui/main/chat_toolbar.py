import streamlit as st
from ui.main.question_helper import render_question_helper


# ==========================================================
# Chat Toolbar
# ==========================================================
def render_chat_toolbar():
    selected_question = None
    col1, spacer, col2, col3 = st.columns([4, 6, 1, 1])

    # ------------------------------------------------------
    # Suggested Questions
    # ------------------------------------------------------
    with col1:
        selected_question = render_question_helper()

    # ------------------------------------------------------
    # Clear Chat
    # ------------------------------------------------------
    with col2:
        if st.button("🗑", help="Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.debug = None
            st.rerun()

    # ------------------------------------------------------
    # Export Chat
    # ------------------------------------------------------
    with col3:
        st.button(
            "📤", help="Export conversation", disabled=True, use_container_width=True
        )
    return selected_question
