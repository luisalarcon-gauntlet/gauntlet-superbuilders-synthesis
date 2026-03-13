"""
Pydantic models for authentication
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class RegisterRequest(BaseModel):
    """Request model for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=1, max_length=255)


class LoginRequest(BaseModel):
    """Request model for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response model (excludes password)"""
    id: UUID
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class AuthResponse(BaseModel):
    """Authentication response model"""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


# StandardResponse moved to common.py for reuse across all endpoints
