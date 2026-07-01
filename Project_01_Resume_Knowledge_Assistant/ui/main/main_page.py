from ui.main.chat_history import render_chat_history
from ui.main.chat_input import render_chat_input
from ui.main.chat_toolbar import render_chat_toolbar


# ==========================================================
# Main Page
# ==========================================================
def render_main_page(system):
    # ------------------------------------------------------
    # Chat History
    # ------------------------------------------------------
    render_chat_history()

    # ------------------------------------------------------
    # Chat Input
    # ------------------------------------------------------
    typed_question = render_chat_input()

    # ------------------------------------------------------
    # Toolbar
    # ------------------------------------------------------
    suggested_question = render_chat_toolbar()

    # ------------------------------------------------------
    # Final Question
    # ------------------------------------------------------
    question = typed_question or suggested_question

    # ------------------------------------------------------
    # Controller
    # ------------------------------------------------------
    if question:
        #
        # Next Sprint
        #
        # handle_question(
        #     question,
        #     system,
        # )
        print(question)
