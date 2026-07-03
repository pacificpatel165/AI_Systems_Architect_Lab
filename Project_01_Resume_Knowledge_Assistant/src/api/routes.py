from fastapi import APIRouter, Request

from src.api.schemas import (
    HealthResponse,
    ModelResponse,
    QuestionRequest,
    QuestionResponse,
    StatsResponse,
)
from src.config import EMBEDDING_MODEL_NAME, RERANKER_MODEL_NAME, LLM_MODEL_NAME
from src.logger import get_logger
from src.config import PROJECT_VERSION

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Resume Assistant"])


# ==========================================================
# Root
# ==========================================================
@router.get("/")
def root():
    return {
        "message": "Resume Knowledge Assistant API",
        "version": PROJECT_VERSION,
        "docs": "/docs",
    }


# ==========================================================
# Health
# ==========================================================
@router.get("/health", response_model=HealthResponse)
def health():
    logger.info("Health endpoint called")
    return HealthResponse(status="healthy", version=PROJECT_VERSION)


# ==========================================================
# Models
# ==========================================================
@router.get("/models", response_model=ModelResponse)
def models():
    logger.info("Model information requested")
    return ModelResponse(
        embedding=EMBEDDING_MODEL_NAME, reranker=RERANKER_MODEL_NAME, llm=LLM_MODEL_NAME
    )


# ==========================================================
# Statistics
# ==========================================================
@router.get("/stats", response_model=StatsResponse)
def stats(request: Request):
    logger.info("System statistics requested")
    system = request.app.state.system
    return StatsResponse(
        documents=system.stats["pages_loaded"],
        chunks=system.stats["chunks_created"],
        vectors=system.stats["vectors_stored"],
    )


# ==========================================================
# Ask
# ==========================================================
@router.post("/ask", response_model=QuestionResponse)
def ask(request: Request, body: QuestionRequest):
    logger.info("Question received: %s", body.question)
    system = request.app.state.system
    response = system.assistant.ask(body.question)
    logger.info("Question processed successfully in %.3f sec", response.latency)
    return QuestionResponse(
        answer=response.answer, sources=response.sources, latency=response.latency
    )
