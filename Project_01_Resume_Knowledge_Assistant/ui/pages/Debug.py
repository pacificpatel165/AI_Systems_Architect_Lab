import streamlit as st
from ui.core.layout import render_layout
from ui.core.app_state import get_system
from ui.debug.debug_page import render_debug_page

st.set_page_config(page_title="Debug Dashboard", page_icon="⚙", layout="wide")

system = get_system()
render_layout(system)
render_debug_page()
