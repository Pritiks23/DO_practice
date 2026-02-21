"""
Configuration management for the application.
"""
import os
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )
    
    # Server settings
    port: int = 3000
    node_env: str = "development"
    
    # API settings
    api_version: str = "v1"
    api_prefix: str = "/api"
    
    # Logging settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    
    # CORS settings
    cors_origin: str = "*"


config = Settings()
