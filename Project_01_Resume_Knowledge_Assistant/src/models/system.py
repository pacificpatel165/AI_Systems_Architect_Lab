from dataclasses import dataclass
from src.models.model_info import ModelInfo

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
    model_info: ModelInfo
