import os
import sys
import json
import logging
import logging.handlers
from pathlib import Path
from typing import Any, Dict

# Get the base directory for logs
LOGS_DIR = Path(os.getenv("RAVENCHAIN_LOGS_DIR", "logs"))
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Log file paths
MAIN_LOG = LOGS_DIR / "ravenchain.log"
ERROR_LOG = LOGS_DIR / "error.log"
DEBUG_LOG = LOGS_DIR / "debug.log"


class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after gathering all the log record args
    """

    def __init__(self, **kwargs: Any) -> None:
        self.default_fields = kwargs
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        message = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields from record
        if hasattr(record, "props"):
            message.update(record.props)

        # Add default fields
        if self.default_fields:
            message.update(self.default_fields)

        if record.exc_info:
            message["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(message)


class StructuredLogger(logging.Logger):
    """
    Custom logger class that allows structured logging with additional properties
    """

    def _log(
        self,
        level: int,
        msg: str,
        args: tuple,
        exc_info: Any = None,
        extra: Dict = None,
        stack_info: bool = False,
        **kwargs: Any,
    ) -> None:
        if extra is None:
            extra = {}
        if kwargs:
            extra["props"] = kwargs
        super()._log(level, msg, args, exc_info, extra, stack_info)


def setup_logging(
    service_name: str = "ravenchain",
    log_level: str = None,
    json_output: bool = False,
    console_output: bool = True,
) -> logging.Logger:
    """
    Set up logging configuration

    Args:
        service_name: Name of the service (default: 'ravenchain')
        log_level: Override default log level from environment
        json_output: Whether to output logs in JSON format
        console_output: Whether to output logs to console
    """
    # Register our custom logger class
    logging.setLoggerClass(StructuredLogger)

    # Determine log level from environment or parameter
    log_level = log_level or os.getenv("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(numeric_level)
    logger.handlers = []  # Reset handlers if they exist

    # Formatter
    if json_output:
        formatter = JSONFormatter(service=service_name)
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"
        )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Main rotating file handler
    main_handler = logging.handlers.RotatingFileHandler(
        MAIN_LOG, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
    )
    main_handler.setFormatter(formatter)
    logger.addHandler(main_handler)

    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    # Debug file handler (only active if debug level is set)
    if numeric_level <= logging.DEBUG:
        debug_handler = logging.handlers.RotatingFileHandler(
            DEBUG_LOG, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        logger.addHandler(debug_handler)

    return logger


# Example usage:
# logger = setup_logging('ravenchain.cli', json_output=True)
# logger.info("Starting application", version="1.0.0", env="production")
# logger.error("Database connection failed", db_host="localhost", retry_count=3)
