import streamlit as st


def status(enabled: bool, title: str):
    if enabled:
        st.success(f"🟢 {title}")
    else:
        st.info(f"⚪ {title} (Skipped)")