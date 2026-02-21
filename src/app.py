"""
FastAPI application setup.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.config import config
from src.middleware import error_handler, request_logger
from src.health_routes import router as health_router
from src.data_routes import router as data_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="DO Practice API",
        description="Production-ready REST API service for data ingestion and processing",
        version="1.0.0",
        docs_url=f"{config.api_prefix}/{config.api_version}/docs",
        redoc_url=f"{config.api_prefix}/{config.api_version}/redoc",
        openapi_url=f"{config.api_prefix}/{config.api_version}/openapi.json",
    )

    # CORS middleware
    origins = config.cors_origin.split(",") if config.cors_origin != "*" else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom middleware
    app.middleware("http")(request_logger)
    app.middleware("http")(error_handler)

    # Register routes
    app.include_router(
        health_router, prefix=f"{config.api_prefix}/{config.api_version}", tags=["health"]
    )
    app.include_router(
        data_router, prefix=f"{config.api_prefix}/{config.api_version}/data", tags=["data"]
    )

    # 404 handler
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "message": f"Route {request.method} {request.url.path} not found",
                    "statusCode": 404,
                }
            },
        )

    return app
