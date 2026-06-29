from dataclasses import dataclass


@dataclass
class ModelInfo:
    embedding: str
    reranker: str
    llm: str
