"""
Middleware for error handling and logging.
"""
import time
from typing import Callable
from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.exceptions import AppError
from src.logger import logger


async def error_handler(request: Request, call_next: Callable):
    """
    Global error handling middleware.
    
    Args:
        request: FastAPI request
        call_next: Next middleware/route handler
        
    Returns:
        Response
    """
    try:
        response = await call_next(request)
        return response
    except AppError as err:
        logger.error(
            f"AppError occurred: {err.message}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": err.status_code,
            }
        )
        
        error_response = {
            "error": {
                "message": err.message,
                "statusCode": err.status_code,
            }
        }
        
        if err.details:
            error_response["error"]["details"] = err.details
        
        return JSONResponse(
            status_code=err.status_code,
            content=error_response
        )
    except ValueError as err:
        # Handle ValueError from services
        if "not found" in str(err):
            status_code = status.HTTP_404_NOT_FOUND
        else:
            status_code = status.HTTP_400_BAD_REQUEST
        
        logger.error(
            f"ValueError occurred: {str(err)}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
            }
        )
        
        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "message": str(err),
                    "statusCode": status_code,
                }
            }
        )
    except Exception as err:
        logger.error(
            f"Unexpected error occurred: {str(err)}",
            extra={
                "method": request.method,
                "path": request.url.path,
            },
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "message": "Internal Server Error",
                    "statusCode": 500,
                }
            }
        )


async def request_logger(request: Request, call_next: Callable):
    """
    Middleware for logging requests.
    
    Args:
        request: FastAPI request
        call_next: Next middleware/route handler
        
    Returns:
        Response
    """
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2)
        }
    )
    
    return response
