"""
User model - stores basic user information for students
"""
from models.base import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel):
    """User model for students using the math tutor"""
    __tablename__ = 'users'

    name = Column(String(255), nullable=False)

    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
