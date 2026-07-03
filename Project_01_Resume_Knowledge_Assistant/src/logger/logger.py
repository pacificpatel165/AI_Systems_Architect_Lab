"""
Application Logging

Provides a centralized logger for the application.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ==========================================================
# Log Directory
# ==========================================================
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


# ==========================================================
# Logger Factory
# ==========================================================
def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Example:
        logger = get_logger(__name__)
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ------------------------------------------------------
    # Console
    # ------------------------------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # ------------------------------------------------------
    # File
    # ------------------------------------------------------
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger
