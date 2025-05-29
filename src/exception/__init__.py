import logging
import sys
import traceback
from types import TracebackType
from typing import Optional, Type


def get_error_details(exc_type: Type[BaseException],
                      exc_value: BaseException,
                      exc_tb: Optional[TracebackType]) -> str:
    """
    Extracts detailed error information including file name, line number, and message.

    Args:
        exc_type (Type[BaseException]): The type of the exception.
        exc_value (BaseException): The exception instance.
        exc_tb (TracebackType): The traceback object.

    Returns:
        str: A formatted error message string.
    """
    if exc_tb:
        filename = exc_tb.tb_frame.f_code.co_filename
        lineno = exc_tb.tb_lineno
    else:
        filename = "Unknown"
        lineno = -1

    error_message = (
        f"Exception occurred in file [{filename}] at line [{lineno}]: {exc_value}"
    )
    
    # Log it here with full traceback for debugging
    logging.error(error_message)
    logging.debug("Full traceback:\n%s", "".join(traceback.format_exception(exc_type, exc_value, exc_tb)))
    
    return error_message


class CustomException(Exception):
    """
    Custom exception class to wrap and log exceptions with detailed traceback.
    Suitable for ML pipelines and production systems.
    """

    def __init__(self, original_exception: Exception):
        """
        Args:
            original_exception (Exception): The actual exception instance.
        """
        exc_type, exc_value, exc_tb = sys.exc_info()
        self.error_message = get_error_details(exc_type, exc_value or original_exception, exc_tb)
        super().__init__(self.error_message)

    def __str__(self) -> str:
        return self.error_message
