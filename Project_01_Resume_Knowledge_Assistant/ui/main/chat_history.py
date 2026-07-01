import streamlit as st


# ==========================================================
# Chat History
# ==========================================================
def render_chat_history():
    messages = st.session_state.get("messages", [])
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
