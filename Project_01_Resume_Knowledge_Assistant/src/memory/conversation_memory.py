import json
import time
from pathlib import Path

# ==========================================================
# Conversation Memory
# ==========================================================
conversation_memory = []

# ==========================================================
# Build Memory Context
# ==========================================================
def build_memory_context(conversation_memory, max_turns=5):
    memory_context = ""
    recent_turns = conversation_memory[-max_turns:]
    for turn_num, turn in enumerate(recent_turns, start=1):
        memory_context += f"""
            Conversation Turn: {turn_num}
            User Question: {turn['question']}
            Assistant Answer: {turn['answer']}
            {'-'*60}
        """
    return memory_context


# ==========================================================
# Save Memory
# ==========================================================
def save_to_memory(question, answer, top_indices, chunks, conversation_memory):
    retrieved_chunks = []
    for idx in top_indices:
        retrieved_chunks.append(
            {
                "parent_id": chunks[idx]["parent_id"],
                "source_file": chunks[idx]["source_file"],
                "document_type": chunks[idx]["document_type"],
                "page_number": chunks[idx]["page_number"],
                "text": chunks[idx]["text"][:300],
            }
        )
    conversation_memory.append(
        {
            "question": question,
            "answer": answer,
            "retrieved_chunks": retrieved_chunks,
            "timestamp": time.time(),
        }
    )


# ==========================================================
# Memory Statistics
# ==========================================================
def print_memory_stats(conversation_memory):
    print()
    print("=" * 80)
    print("MEMORY STATISTICS")
    print("=" * 80)

    print(f"Total Turns: " f"{len(conversation_memory)}")

    if len(conversation_memory) > 0:
        print()
        print("Last Question:")
        print(conversation_memory[-1]["question"])
