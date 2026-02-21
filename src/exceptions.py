"""
Exception classes for the application.
"""
from typing import Any, Optional


class AppError(Exception):
    """Base application error with status code."""
    
    def __init__(
        self, 
        status_code: int, 
        message: str, 
        details: Optional[Any] = None
    ):
        """
        Initialize the error.
        
        Args:
            status_code: HTTP status code
            message: Error message
            details: Optional additional details
        """
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(self.message)
