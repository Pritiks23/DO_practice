"""
Logger utility for structured logging.
"""

import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
from src.config import config


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "msg": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class ColoredConsoleFormatter(logging.Formatter):
    """Colored console formatter for human-readable logs."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, self.RESET)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        msg = f"{timestamp} [{color}{record.levelname}{self.RESET}]: {record.getMessage()}"

        # Add extra fields if present
        if hasattr(record, "extra_data"):
            meta_str = json.dumps(record.extra_data, indent=2)
            msg += f" {meta_str}"

        return msg


# Create logger
logger = logging.getLogger("do_practice")
logger.setLevel(getattr(logging, config.log_level.upper()))

# Console handler with colored output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(ColoredConsoleFormatter())
logger.addHandler(console_handler)

# Remove default handlers
logger.propagate = False
