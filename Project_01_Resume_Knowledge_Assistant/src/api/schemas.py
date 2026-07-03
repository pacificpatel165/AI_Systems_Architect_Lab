from pydantic import BaseModel


# ==========================================================
# Request
# ==========================================================
class QuestionRequest(BaseModel):
    question: str


# ==========================================================
# Response
# ==========================================================
class QuestionResponse(BaseModel):
    answer: str
    sources: list
    latency: float


# ==========================================================
# Health
# ==========================================================
class HealthResponse(BaseModel):
    status: str
    version: str


# ==========================================================
# Models
# ==========================================================
class ModelResponse(BaseModel):
    embedding: str
    reranker: str
    llm: str


# ==========================================================
# Statistics
# ==========================================================
class StatsResponse(BaseModel):
    documents: int
    chunks: int
    vectors: int