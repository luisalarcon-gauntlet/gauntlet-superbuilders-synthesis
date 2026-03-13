"""
Common Pydantic models used across the API
"""
from pydantic import BaseModel
from typing import Optional, Any


class StandardResponse(BaseModel):
    """Standard API response wrapper - generic to support any data type"""
    data: Optional[Any] = None
    error: Optional[str] = None
