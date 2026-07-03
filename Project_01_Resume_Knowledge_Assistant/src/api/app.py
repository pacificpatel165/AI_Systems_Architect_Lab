from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.routes import router
from src.bootstrap import initialize_system
from src.logger import get_logger
from src.config import PROJECT_VERSION

logger = get_logger(__name__)


# ==========================================================
# Application Lifespan
# ==========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Resume Knowledge Assistant API")
    app.state.system = initialize_system()
    logger.info("API initialization completed")
    yield
    logger.info("API shutdown")


# ==========================================================
# FastAPI Application
# ==========================================================
app = FastAPI(
    title="Resume Knowledge Assistant API",
    description="REST API for Resume Knowledge Assistant",
    version=PROJECT_VERSION,
    lifespan=lifespan,
)

app.include_router(router)