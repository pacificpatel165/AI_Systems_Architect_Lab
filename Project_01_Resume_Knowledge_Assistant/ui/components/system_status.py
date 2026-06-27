import streamlit as st


# ==========================================================
# System Status
# ==========================================================
def render_system_status(stats):
    st.sidebar.subheader("⚙️ System Status")
    st.sidebar.success("System Ready")

    st.sidebar.write(f"📄 Pages Loaded : {stats['pages_loaded']}")
    st.sidebar.write(f"🧩 Chunks : {stats['chunks_created']}")
    st.sidebar.write(f"🗂️ Vectors : {stats['vectors_stored']}")

    st.sidebar.divider()
