from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel
import uuid

class LessonStep(BaseModel):
    __tablename__ = 'lesson_steps'
    
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id'), nullable=False)
    step_number = Column(Integer, nullable=False)
    step_type = Column(String(50), nullable=False)  # 'exploration', 'instruction', 'question', 'check'
    tutor_message = Column(Text, nullable=False)
    expected_action = Column(String(100), nullable=True)
    success_message = Column(Text, nullable=True)
    hint_message = Column(Text, nullable=True)
    
    # Relationships
    lesson = relationship("Lesson", back_populates="steps")
    sessions = relationship("UserSession", foreign_keys="[UserSession.current_step_id]", back_populates="current_step")
    manipulative_interactions = relationship("ManipulativeInteraction", back_populates="step")
    conversation_logs = relationship("ConversationLog", back_populates="step")
