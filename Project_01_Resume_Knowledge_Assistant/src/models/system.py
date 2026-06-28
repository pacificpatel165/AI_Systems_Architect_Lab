from dataclasses import dataclass


# ==========================================================
# System State
# ==========================================================
@dataclass
class SystemState:
    assistant: object
    stats: dict
    chunks: list
    parent_documents: dict
    index: object
    embedding_model: object
    reranker: object
    llm_model: object
