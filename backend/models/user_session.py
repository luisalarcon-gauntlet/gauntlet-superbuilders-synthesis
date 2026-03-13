from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel

class UserSession(BaseModel):
    __tablename__ = 'user_sessions'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id'), nullable=False)
    status = Column(String(50), nullable=False)  # 'in_progress', 'completed', 'abandoned'
    current_step_id = Column(UUID(as_uuid=True), ForeignKey('lesson_steps.id'), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    lesson = relationship("Lesson", back_populates="sessions")
    current_step = relationship("LessonStep", foreign_keys=[current_step_id], back_populates="sessions")
    manipulative_interactions = relationship("ManipulativeInteraction", back_populates="session")
    conversation_logs = relationship("ConversationLog", back_populates="session")
