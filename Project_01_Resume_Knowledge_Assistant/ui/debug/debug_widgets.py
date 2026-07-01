import streamlit as st


# ==========================================================
# Status Widget
# ==========================================================
def status(enabled, label):
    if enabled:
        st.success(f"✅ {label}")
    else:
        st.info(f"➖ {label}")
