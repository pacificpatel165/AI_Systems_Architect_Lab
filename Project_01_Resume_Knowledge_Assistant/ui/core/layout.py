from ui.core.theme import load_css
from ui.core.header import render_header
from ui.core.sidebar import render_sidebar


# ==========================================================
# Page Layout
# ==========================================================
def render_layout(system):
    load_css()
    render_header()
    render_sidebar(system)
