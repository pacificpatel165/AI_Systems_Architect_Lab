from src.rewriting.query_rewriter import is_followup_question

# ==========================================================
# Query Types
# ==========================================================
GENERAL_QUERY = "general"
FOLLOWUP_QUERY = "followup"
DOCUMENT_QUERY = "document"
KEYWORD_QUERY = "keyword"


# ==========================================================
# Classify Question
# ==========================================================
def classify_question(question):
    lower = question.lower()
    # --------------------------------------
    # Follow-up Question
    # --------------------------------------
    if is_followup_question(question):
        return FOLLOWUP_QUERY

    # --------------------------------------
    # Document Questions
    # --------------------------------------
    if any(
        word in lower
        for word in ["certificate", "certification", "resume", "project", "note"]
    ):
        return DOCUMENT_QUERY

    # --------------------------------------
    # Keyword Questions
    # --------------------------------------
    if len(question.split()) <= 2:
        return KEYWORD_QUERY

    # --------------------------------------
    # General
    # --------------------------------------
    return GENERAL_QUERY


# ==========================================================
# Retrieval Strategy
# ==========================================================
def get_retrieval_strategy(query_type):

    if query_type == FOLLOWUP_QUERY:
        return {"rewrite": True, "metadata": False, "parent": True, "compression": True}
    if query_type == DOCUMENT_QUERY:
        return {"rewrite": False, "metadata": True, "parent": True, "compression": True}
    if query_type == KEYWORD_QUERY:
        return {
            "rewrite": False,
            "metadata": False,
            "parent": False,
            "compression": False,
        }
    return {"rewrite": False, "metadata": False, "parent": True, "compression": True}


# ==========================================================
# Strategy Debug
# ==========================================================
def print_strategy(question, query_type, strategy):
    print()
    print("=" * 80)
    print("RETRIEVAL STRATEGY")
    print("=" * 80)
    print(f"Question   : {question}")
    print(f"Type       : {query_type}")
    print()
    for key, value in strategy.items():
        print(f"{key:<15}: {value}")
