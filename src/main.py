"""
Main entry point for the application.
"""

import signal
import sys
import uvicorn
from src.app import create_app
from src.config import config
from src.logger import logger

app = create_app()


def handle_shutdown(signum, frame):
    """Handle graceful shutdown."""
    logger.info(f"Signal {signum} received, shutting down gracefully")
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    logger.info(
        "Server starting",
        extra={"port": config.port, "env": config.node_env, "api_version": config.api_version},
    )

    # Run the application
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=config.port,
        log_level=config.log_level.lower(),
        reload=config.node_env == "development",
    )
