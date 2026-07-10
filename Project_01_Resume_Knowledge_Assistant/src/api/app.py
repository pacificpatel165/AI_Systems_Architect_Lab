from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes import router
from src.bootstrap import initialize_system
from src.config import PROJECT_NAME, PROJECT_VERSION
from src.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# Application Lifespan
# ==========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s API version %s", PROJECT_NAME, PROJECT_VERSION)

    try:
        app.state.system = initialize_system()
        logger.info("%s API startup completed", PROJECT_NAME)
        yield
    except Exception:
        logger.exception("%s API lifecycle failure", PROJECT_NAME)
        raise
    finally:
        logger.info("%s API shutdown completed", PROJECT_NAME)


# ==========================================================
# FastAPI Application
# ==========================================================
app = FastAPI(
    title=f"{PROJECT_NAME} API",
    description="REST API for Resume Knowledge Assistant",
    version=PROJECT_VERSION,
    lifespan=lifespan,
)


# ==========================================================
# API Routes
# ==========================================================
app.include_router(router)
