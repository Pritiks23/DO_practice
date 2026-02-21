"""
Data management endpoints.
"""

from fastapi import APIRouter, Query, status
from src.types import IngestDataRequest
from src.data_service import data_service
from src.exceptions import AppError

router = APIRouter()


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def ingest_data(request: IngestDataRequest):
    """
    Ingest new data.

    Args:
        request: Data ingestion request

    Returns:
        Success response with created record
    """
    if not request.data or not isinstance(request.data, dict):
        raise AppError(400, "Invalid data: data must be an object")

    record = await data_service.ingest_data(request.data, request.metadata)

    return {"success": True, "data": record.model_dump(mode="json")}


@router.post("/{record_id}/process", response_model=dict)
async def process_data(record_id: str):
    """
    Process a data record.

    Args:
        record_id: ID of the record to process

    Returns:
        Success response with processed record
    """
    try:
        processed_record = await data_service.process_data(record_id)

        return {"success": True, "data": processed_record.model_dump(mode="json")}
    except ValueError as e:
        if "not found" in str(e):
            raise AppError(404, str(e))
        raise


@router.get("/{record_id}", response_model=dict)
async def get_data(record_id: str):
    """
    Get a specific data record.

    Args:
        record_id: ID of the record to retrieve

    Returns:
        Success response with the record
    """
    record = await data_service.get_data(record_id)

    if not record:
        raise AppError(404, f"Record with id {record_id} not found")

    return {"success": True, "data": record.model_dump(mode="json")}


@router.get("", response_model=dict)
async def get_all_data(
    limit: int = Query(default=100, ge=1, le=1000), offset: int = Query(default=0, ge=0)
):
    """
    Get all data records with pagination.

    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip

    Returns:
        Success response with records and pagination info
    """
    records = await data_service.get_all_data(limit, offset)
    stats = data_service.get_stats()

    return {
        "success": True,
        "data": [record.model_dump(mode="json") for record in records],
        "pagination": {"limit": limit, "offset": offset, "total": stats["total"]},
        "stats": stats,
    }


@router.delete("/{record_id}", response_model=dict)
async def delete_data(record_id: str):
    """
    Delete a data record.

    Args:
        record_id: ID of the record to delete

    Returns:
        Success response
    """
    deleted = await data_service.delete_data(record_id)

    if not deleted:
        raise AppError(404, f"Record with id {record_id} not found")

    return {"success": True, "message": f"Record with id {record_id} deleted successfully"}
