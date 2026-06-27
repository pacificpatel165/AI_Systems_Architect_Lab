import streamlit as st
from ui.quick_questions import QUICK_QUESTIONS


# ==========================================================
# Sidebar
# ==========================================================
def render_sidebar():
    st.sidebar.header("🚀 Try a Question")
    selected_question = None
    for category, questions in QUICK_QUESTIONS.items():
        with st.sidebar.expander(category):
            for question in questions:
                if st.button(
                    question,
                    key=f"{category}_{question}",
                    use_container_width=True,
                ):
                    selected_question = question

    st.sidebar.divider()

    if st.sidebar.button(
        "🗑 Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        if "debug" in st.session_state:
            del st.session_state.debug
        st.rerun()

    return selected_question
