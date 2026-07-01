import streamlit as st


# ==========================================================
# Handle User Question
# ==========================================================
def handle_question(question, system):
    """
    Process a user question and update the UI state.

    Responsibilities:
        • Call Resume Assistant
        • Save conversation
        • Save debug information
    """

    # ------------------------------------------------------
    # Ignore Empty Questions
    # ------------------------------------------------------
    if not question:
        return

    # ------------------------------------------------------
    # Initialize Session State
    # ------------------------------------------------------
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("debug", None)

    # ------------------------------------------------------
    # User Message
    # ------------------------------------------------------
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # ------------------------------------------------------
    # Assistant Response
    # ------------------------------------------------------
    response = system.assistant.ask(question)

    # ------------------------------------------------------
    # Save Debug
    # ------------------------------------------------------
    st.session_state.debug = response.debug

    # ------------------------------------------------------
    # Assistant Message
    # ------------------------------------------------------
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "sources": response.sources,
            "latency": response.latency,
        }
    )

    # No st.rerun() here.
