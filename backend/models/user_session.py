"""
UserSession model - tracks individual learning sessions
"""
from models.base import BaseModel
from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class UserSession(BaseModel):
    """UserSession model for tracking learning sessions"""
    __tablename__ = 'user_sessions'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    status = Column(String(50), nullable=False)  # 'in_progress', 'completed', 'abandoned'
    current_step_id = Column(UUID(as_uuid=True), ForeignKey('lesson_steps.id', ondelete='SET NULL'), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="sessions")
    lesson = relationship("Lesson", back_populates="sessions")
    current_step = relationship("LessonStep", back_populates="sessions", foreign_keys=[current_step_id])
    manipulative_interactions = relationship("ManipulativeInteraction", back_populates="session", cascade="all, delete-orphan")
    conversation_logs = relationship("ConversationLog", back_populates="session", cascade="all, delete-orphan")
