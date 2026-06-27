import streamlit as st


# ==========================================================
# Sources
# ==========================================================
def render_sources(sources):
    with st.expander("📄 Sources"):
        for source in sources:
            st.write(f"**{source['source_file']}** " f"(Page {source['page']})")
