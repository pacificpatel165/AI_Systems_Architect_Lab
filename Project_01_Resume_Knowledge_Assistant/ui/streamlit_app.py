import streamlit as st
from src.bootstrap import initialize_system

st.set_page_config(
    page_title="Resume Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Resume Knowledge Assistant")
st.success("Streamlit is working!")

if "assistant" not in st.session_state:
    with st.spinner("Initializing AI Assistant..."):
        assistant, stats = initialize_system()
        st.session_state.assistant = assistant
        st.session_state.stats = stats

st.sidebar.title("System Status")
stats = st.session_state.stats
st.sidebar.success("System Ready")
st.sidebar.write(f"Pages Loaded : {stats['pages_loaded']}")
st.sidebar.write(f"Chunks : {stats['chunks_created']}")
st.sidebar.write(f"Vectors : {stats['vectors_stored']}")
