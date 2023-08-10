## utils.py
import logging
from typing import Any, Dict

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """Set up logger."""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def handle_error(logger: logging.Logger, error: Exception) -> Dict[str, Any]:
    """Handle error by logging and returning error message."""
    logger.error(str(error))
    return {"error": str(error)}
