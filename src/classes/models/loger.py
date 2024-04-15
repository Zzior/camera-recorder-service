import logging
from pathlib import Path
from logging import Logger


def setup_logger(save_path: Path) -> Logger:
    """Set up and return a configured logger."""
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(save_path)
    file_handler.setLevel(logging.INFO)
    log_format = """----------------------------------------------------------------------------------------------------
    %(asctime)s - %(name)s - %(levelname)s - %(message)s
    ----------------------------------------------------------------------------------------------------"""
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    return logger
