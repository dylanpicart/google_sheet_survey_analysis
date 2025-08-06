import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(
    log_stage,
    log_level=logging.INFO,
    base_log_dir="logs",
    max_bytes=5 * 1024 * 1024,
    backup_count=3,
    separate_error_log=True,
    log_to_file=True,
):
    """
    log_stage: 'extract', 'transform', or 'load'
    base_log_dir: Top-level logs directory (default: 'logs')
    """
    logger = logging.getLogger(log_stage)
    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Directory for this stage
    log_dir = os.path.join(base_log_dir, log_stage)
    if log_to_file:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{log_stage}.log")
        main_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        main_handler.setFormatter(formatter)
        logger.addHandler(main_handler)

        if separate_error_log:
            error_file = os.path.join(log_dir, f"{log_stage}_error.log")
            error_handler = RotatingFileHandler(
                error_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
            )
            error_handler.setLevel(logging.WARNING)
            error_handler.setFormatter(formatter)
            logger.addHandler(error_handler)
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.propagate = False
    return logger
