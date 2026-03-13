from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel
import uuid

class ManipulativeInteraction(BaseModel):
    __tablename__ = 'manipulative_interactions'
    
    session_id = Column(UUID(as_uuid=True), ForeignKey('user_sessions.id'), nullable=False)
    step_id = Column(UUID(as_uuid=True), ForeignKey('lesson_steps.id'), nullable=False)
    interaction_type = Column(String(50), nullable=False)  # 'drag', 'combine', 'split', 'compare'
    fraction_value = Column(String(20), nullable=False)
    position_x = Column(Integer, nullable=True)
    position_y = Column(Integer, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    session = relationship("UserSession", back_populates="manipulative_interactions")
    step = relationship("LessonStep", back_populates="manipulative_interactions")
