from src.logger import get_logger

logger = get_logger(__name__)

# ==========================================================
# Follow-Up Words
# ==========================================================
FOLLOWUP_WORDS = {
    "it",
    "its",
    "that",
    "this",
    "they",
    "them",
    "their",
    "those",
    "these",
    "he",
    "him",
    "his",
    "she",
    "her",
    "there",
    "then",
    "which",
    "who",
    "where",
    "when",
}


# ==========================================================
# Detect Follow-Up Question
# ==========================================================
def is_followup_question(question):
    words = question.lower().replace("?", "").split()
    followup = any(word in FOLLOWUP_WORDS for word in words)
    logger.debug("Follow-up detection: %s", followup)
    return followup


# ==========================================================
# Recent Context
# ==========================================================
def get_recent_context(conversation_memory, max_turns=3):
    if len(conversation_memory) == 0:
        logger.debug("Conversation memory is empty.")
        return []

    logger.debug(
        "Using last %d conversation turns", min(max_turns, len(conversation_memory))
    )
    return conversation_memory[-max_turns:]


# ==========================================================
# Rewrite Query
# ==========================================================
def rewrite_query(question, conversation_memory):
    logger.debug("Starting query rewriting")

    # ------------------------------------------------------
    # No Memory
    # ------------------------------------------------------
    if len(conversation_memory) == 0:
        logger.debug("No conversation memory available. " "Skipping query rewrite.")
        return question

    # ------------------------------------------------------
    # Independent Question
    # ------------------------------------------------------
    if not is_followup_question(question):
        logger.debug("Independent question detected. " "No rewrite required.")
        return question

    # ------------------------------------------------------
    # Build Context
    # ------------------------------------------------------
    recent_turns = get_recent_context(conversation_memory, max_turns=3)
    previous_questions = []
    previous_answers = []
    retrieved_context = []
    for turn in recent_turns:
        previous_questions.append(turn["question"])
        previous_answers.append(turn["answer"])
        for chunk in turn["retrieved_chunks"]:
            retrieved_context.append(chunk["text"])
    rewritten_query = f"""
        Current Question: {question}
        Previous Questions:
        {' | '.join(previous_questions)}
        Previous Answers:
        {' | '.join(previous_answers)}
        Relevant Context:
        {' '.join(retrieved_context[:3])}
    """
    logger.info(
        "Query rewritten using %d conversation turns and %d retrieved chunks",
        len(recent_turns),
        len(retrieved_context),
    )
    logger.debug("Rewritten query length: %d characters", len(rewritten_query))
    return rewritten_query


# ==========================================================
# Debug
# ==========================================================
def print_rewrite_debug(original_question, rewritten_query):
    print()
    print("=" * 80)
    print("QUERY REWRITING")
    print("=" * 80)

    print()

    print("Original Question")
    print("-" * 80)
    print(original_question)

    print()

    print("Rewritten Query")
    print("-" * 80)
    print(rewritten_query)
