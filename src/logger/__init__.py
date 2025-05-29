import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from from_root import from_root  

# Constants
LOG_DIR_NAME = 'logs'
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Keep 3 backup files

def get_log_file_path() -> str:
    """
    Constructs a timestamped log file path in the root/logs directory.
    """
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    log_dir = os.path.join(from_root(), LOG_DIR_NAME)
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, f"{timestamp}.log")

def configure_logger(name: str = '', level: int = logging.DEBUG) -> logging.Logger:
    """
    Configures and returns a logger with both console and rotating file handlers.

    Args:
        name (str): Name of the logger. Use '' for root logger.
        level (int): Logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers if this function is called multiple times
    if logger.handlers:
        return logger

    log_file_path = get_log_file_path()
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    # File Handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Example usage
logger = configure_logger()
logger.info("Logger has been configured successfully.")
