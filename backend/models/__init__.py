"""SQLAlchemy models for Synthesis Math Tutor"""
try:
    from backend.models.base import Base, BaseModel, TimestampMixin
    from backend.models.user import User
    from backend.models.lesson import Lesson
    from backend.models.lesson_step import LessonStep
    from backend.models.user_session import UserSession
    from backend.models.manipulative_interaction import ManipulativeInteraction
    from backend.models.conversation_log import ConversationLog
except ImportError:
    # Fallback for when running from backend directory
    from models.base import Base, BaseModel, TimestampMixin
    from models.user import User
    from models.lesson import Lesson
    from models.lesson_step import LessonStep
    from models.user_session import UserSession
    from models.manipulative_interaction import ManipulativeInteraction
    from models.conversation_log import ConversationLog

__all__ = [
    "Base",
    "BaseModel",
    "TimestampMixin",
    "User",
    "Lesson",
    "LessonStep",
    "UserSession",
    "ManipulativeInteraction",
    "ConversationLog",
]
