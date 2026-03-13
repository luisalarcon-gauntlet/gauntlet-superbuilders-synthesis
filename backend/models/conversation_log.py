"""
ConversationLog model - stores conversational flow between tutor and student
"""
from models.base import BaseModel
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class ConversationLog(BaseModel):
    """ConversationLog model for storing conversation messages"""
    __tablename__ = 'conversation_logs'

    session_id = Column(UUID(as_uuid=True), ForeignKey('user_sessions.id', ondelete='CASCADE'), nullable=False)
    step_id = Column(UUID(as_uuid=True), ForeignKey('lesson_steps.id', ondelete='CASCADE'), nullable=False)
    speaker = Column(String(20), nullable=False)  # 'tutor' or 'student'
    message = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False)  # 'instruction', 'question', 'response', 'encouragement'
    timestamp = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    session = relationship("UserSession", back_populates="conversation_logs")
    step = relationship("LessonStep", back_populates="conversation_logs")
