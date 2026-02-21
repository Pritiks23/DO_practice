"""
Type definitions for the API.
"""

from datetime import datetime
from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, Field


class DataRecord(BaseModel):
    """Model for a data record."""

    id: str
    timestamp: datetime
    data: Dict[str, Any]
    processed: bool = False
    metadata: Optional[Dict[str, Any]] = None


class ProcessingResult(BaseModel):
    """Model for processing result."""

    status: Literal["success", "error"]
    message: Optional[str] = None


class ProcessedData(DataRecord):
    """Model for processed data record."""

    processed: Literal[True] = True
    processingTimestamp: datetime
    processingResult: Optional[ProcessingResult] = None


class IngestDataRequest(BaseModel):
    """Request model for data ingestion."""

    data: Dict[str, Any] = Field(..., description="Data to ingest")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")


class ApiError(BaseModel):
    """Model for API error response."""

    message: str
    statusCode: int
    details: Optional[Any] = None


class HealthCheckResponse(BaseModel):
    """Model for health check response."""

    status: Literal["healthy", "unhealthy"]
    timestamp: datetime
    uptime: float
    version: str
    dependencies: Optional[Dict[str, str]] = None
