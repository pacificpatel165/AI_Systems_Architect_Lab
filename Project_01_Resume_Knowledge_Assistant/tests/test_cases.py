# ==========================================================
# Test Cases
# ==========================================================
TEST_CASES = {
    # ------------------------------------------------------
    # Hybrid Retrieval
    # ------------------------------------------------------
    "retrieval": [
        "Which projects used Python?",
        "What protocols have I worked on?",
        "Which company did I work for?",
    ],
    # ------------------------------------------------------
    # Metadata Filtering
    # ------------------------------------------------------
    "metadata": [
        "Which AWS certifications do I have?",
        "Show my projects.",
        "Summarize my notes.",
    ],
    # ------------------------------------------------------
    # Follow-up Questions
    # ------------------------------------------------------
    "followup": [
        "Which projects used Python?",
        "Which company was that for?",
        "What technologies were used?",
    ],
    # ------------------------------------------------------
    # Parent Retrieval
    # ------------------------------------------------------
    "parent": ["Summarize PMA project.", "Explain TA5K project."],
    # ------------------------------------------------------
    # Context Compression
    # ------------------------------------------------------
    "compression": ["Explain PMA project in detail."],
    # ------------------------------------------------------
    # Unknown Questions
    # ------------------------------------------------------
    "negative": ["What was my salary in 2015?", "Who is my wife?", "Where do I live?"],
}
