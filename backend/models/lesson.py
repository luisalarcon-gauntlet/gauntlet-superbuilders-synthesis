"""
Lesson model - defines available math lessons
"""
from models.base import BaseModel
from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.orm import relationship


class Lesson(BaseModel):
    """Lesson model for available math lessons"""
    __tablename__ = 'lessons'

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    topic = Column(String(100), nullable=False)
    difficulty_level = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    steps = relationship("LessonStep", back_populates="lesson", cascade="all, delete-orphan", order_by="LessonStep.step_number")
    sessions = relationship("UserSession", back_populates="lesson", cascade="all, delete-orphan")
