"""Logging configuration with rotating file handler and console streaming."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from src.config import DEFAULT_LOG_FILE, LOGS_DIR, LOG_MAX_BYTES, LOG_BACKUP_COUNT

def setup_logger(name: str = "visionguard", log_file: Path = None, level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a logger instance with file and console handlers."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # Rotating File Handler
    target_log_file = log_file or DEFAULT_LOG_FILE
    target_log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        target_log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()
