import streamlit as st
from ui.main.question_helper import render_question_helper


# ==========================================================
# Chat Toolbar
# ==========================================================
def render_chat_toolbar():
    """
    Bottom toolbar displayed above the chat input.

    Returns:
        None

    If a suggested question is selected, it is stored in
    session_state and the page is rerun to close the popover.
    """

    col1, spacer, col2, col3 = st.columns([4, 6, 1, 1])

    # ------------------------------------------------------
    # Suggested Questions
    # ------------------------------------------------------
    with col1:
        selected_question = render_question_helper()
        if selected_question:
            st.session_state.selected_question = selected_question
            st.rerun()

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
