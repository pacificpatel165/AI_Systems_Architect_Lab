import streamlit as st


# ==========================================================
# Chat History
# ==========================================================
def render_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📄 Sources"):
                    for source in message["sources"]:
                        st.write(
                            f"• {source['source_file']} " f"(Page {source['page']})"
                        )
