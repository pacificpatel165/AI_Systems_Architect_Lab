import streamlit as st
from ui.main.source_viewer import render_sources


# ==========================================================
# Chat History
# ==========================================================
def render_chat_history():

    messages = st.session_state.get("messages", [])

    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # ----------------------------------------------
            # Assistant Sources
            # ----------------------------------------------
            if message["role"] == "assistant":
                if message.get("sources"):
                    render_sources(message["sources"])
