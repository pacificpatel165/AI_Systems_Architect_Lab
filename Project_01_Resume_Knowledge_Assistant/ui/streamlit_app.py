import streamlit as st
from src.bootstrap import initialize_system
from ui.components.chat import render_chat
from ui.components.sidebar import render_sidebar
from ui.components.system_status import render_system_status
from ui.components.sources import render_sources
from ui.components.debug_dashboard import render_debug_dashboard
from ui.app_state import get_system

# ==========================================================
# Page
# ==========================================================
st.set_page_config(
    page_title="Resume Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
)
st.title("🤖 Resume Knowledge Assistant")
st.caption("AI-powered Resume Knowledge Assistant")


# ==========================================================
# Initialize
# ==========================================================
if "assistant" not in st.session_state:
    system = get_system()
    st.session_state.system = system
    
if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# Sidebar
# ==========================================================
render_system_status(st.session_state.system.stats)
selected_question = render_sidebar()


# ==========================================================
# Chat
# ==========================================================
render_chat()
custom_question = st.chat_input("Ask anything about your resume...")
question = custom_question or selected_question


# ==========================================================
# Ask Assistant
# ==========================================================
if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )
    response = st.session_state.system.assistant.ask(question)
    st.session_state.debug = response.debug
    with st.chat_message("assistant"):
        st.markdown(response.answer)
        render_sources(response.sources)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "sources": response.sources,
            "debug": response.debug,
            "latency": response.latency,
        }
    )
