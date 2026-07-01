import streamlit as st
from ui.main.quick_questions import SUGGESTED_QUESTIONS


# ==========================================================
# Suggested Questions
# ==========================================================
def render_question_helper():
    selected_question = None
    with st.popover("💡 Suggestions", use_container_width=False):
        st.caption("Choose a suggested question")
        for category, questions in SUGGESTED_QUESTIONS.items():
            with st.expander(f"{category} ({len(questions)})"):
                for question in questions:
                    if st.button(
                        question, key=f"{category}_{question}", use_container_width=True
                    ):
                        selected_question = question

    return selected_question
