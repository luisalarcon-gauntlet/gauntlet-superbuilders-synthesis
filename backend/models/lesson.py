from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel

class Lesson(BaseModel):
    __tablename__ = 'lessons'
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    topic = Column(String(100), nullable=False)
    difficulty_level = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    steps = relationship("LessonStep", back_populates="lesson", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="lesson")
