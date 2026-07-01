from ui.main.chat_history import render_chat_history
from ui.main.chat_input import render_chat_input
from ui.main.chat_toolbar import render_chat_toolbar
from ui.main.main_controller import handle_question


# ==========================================================
# Main Page
# ==========================================================
def render_main_page(system):
    # ------------------------------------------------------
    # User Input
    # ------------------------------------------------------
    question = render_chat_input()

    # ------------------------------------------------------
    # Toolbar
    # ------------------------------------------------------
    render_chat_toolbar()

    # ------------------------------------------------------
    # Handle Question
    # ------------------------------------------------------
    if question:
        handle_question(question=question, system=system)

    # ------------------------------------------------------
    # Chat History
    # ------------------------------------------------------
    render_chat_history()
