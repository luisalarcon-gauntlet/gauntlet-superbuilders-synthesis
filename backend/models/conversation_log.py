from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel
import uuid

class ConversationLog(BaseModel):
    __tablename__ = 'conversation_logs'
    
    session_id = Column(UUID(as_uuid=True), ForeignKey('user_sessions.id'), nullable=False)
    step_id = Column(UUID(as_uuid=True), ForeignKey('lesson_steps.id'), nullable=False)
    speaker = Column(String(20), nullable=False)  # 'tutor' or 'student'
    message = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False)  # 'instruction', 'question', 'response', 'encouragement'
    timestamp = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    session = relationship("UserSession", back_populates="conversation_logs")
    step = relationship("LessonStep", back_populates="conversation_logs")
