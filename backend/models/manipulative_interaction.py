"""
ManipulativeInteraction model - records student interactions with digital fraction manipulatives
"""
from models.base import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class ManipulativeInteraction(BaseModel):
    """ManipulativeInteraction model for recording manipulative interactions"""
    __tablename__ = 'manipulative_interactions'

    session_id = Column(UUID(as_uuid=True), ForeignKey('user_sessions.id', ondelete='CASCADE'), nullable=False)
    step_id = Column(UUID(as_uuid=True), ForeignKey('lesson_steps.id', ondelete='CASCADE'), nullable=False)
    interaction_type = Column(String(50), nullable=False)  # 'drag', 'combine', 'split', 'compare'
    fraction_value = Column(String(20), nullable=False)  # e.g., "1/2", "2/4"
    position_x = Column(Integer, nullable=True)
    position_y = Column(Integer, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    session = relationship("UserSession", back_populates="manipulative_interactions")
    step = relationship("LessonStep", back_populates="manipulative_interactions")
