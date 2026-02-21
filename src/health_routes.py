"""
Health check endpoints.
"""

import time
from datetime import datetime
from fastapi import APIRouter
from src.types import HealthCheckResponse

# Track app start time
start_time = time.time()

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status information
    """
    uptime = time.time() - start_time

    return HealthCheckResponse(
        status="healthy", timestamp=datetime.utcnow(), uptime=round(uptime, 2), version="1.0.0"
    )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.

    Returns:
        Readiness status
    """
    return {"status": "ready", "timestamp": datetime.utcnow()}
