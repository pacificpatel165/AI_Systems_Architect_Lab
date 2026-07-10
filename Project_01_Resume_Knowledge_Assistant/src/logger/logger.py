"""
Application Logging

Provides centralized logging configuration for the application.
"""

import logging
from logging.handlers import RotatingFileHandler

from src.config import LOG_DIR, LOG_LEVEL

# ==========================================================
# Log Configuration
# ==========================================================
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ==========================================================
# Logger Factory
# ==========================================================
def get_logger(name: str) -> logging.Logger:
    """
    Return a configured application logger.

    Args:
        name:
            Logger name. Normally __name__.

    Returns:
        Configured logging.Logger instance.
    """

    logger = logging.getLogger(name)

    # ------------------------------------------------------
    # Prevent Duplicate Handlers
    # ------------------------------------------------------
    if logger.handlers:
        return logger

    # ------------------------------------------------------
    # Logger Level
    # ------------------------------------------------------
    log_level = getattr(logging, LOG_LEVEL, logging.INFO)
    logger.setLevel(log_level)

    # ------------------------------------------------------
    # Formatter
    # ------------------------------------------------------
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # ------------------------------------------------------
    # Console Handler
    # ------------------------------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # ------------------------------------------------------
    # File Handler
    # ------------------------------------------------------
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # ------------------------------------------------------
    # Register Handlers
    # ------------------------------------------------------
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger
