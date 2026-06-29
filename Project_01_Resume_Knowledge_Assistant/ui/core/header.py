import streamlit as st


# ==========================================================
# Header
# ==========================================================
def render_header():
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title("🤖 Resume Knowledge Assistant")
        st.caption(
            "Retrieval-Augmented Resume Assistant "
            "using FAISS • Sentence Transformers • Gemini"
        )
    with col2:
        st.empty()
    st.divider()
