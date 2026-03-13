from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    
    name = Column(String(255), nullable=False)
    
    # Relationships
    sessions = relationship("UserSession", back_populates="user")
