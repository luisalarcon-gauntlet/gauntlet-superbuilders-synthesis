"""
Pydantic models for lesson endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class LessonResponse(BaseModel):
    """Lesson response model"""
    id: UUID
    title: str
    description: str
    status: str  # 'not_started', 'in_progress', 'completed'

    class Config:
        from_attributes = True


class BlockModel(BaseModel):
    """Fraction block model"""
    id: str
    type: str  # e.g., "1/2", "1/4", "2/4"
    position: Optional[Dict[str, int]] = None
    color: str
    display: Optional[str] = None
    is_combined: Optional[bool] = False


class WorkspaceModel(BaseModel):
    """Workspace model"""
    width: int
    height: int
    placed_blocks: List[BlockModel] = []


class ManipulativeStateResponse(BaseModel):
    """Manipulative state response"""
    available_blocks: List[BlockModel]
    workspace: WorkspaceModel


class TutorMessageResponse(BaseModel):
    """Tutor message response"""
    id: str
    text: str
    type: str  # 'instruction', 'encouragement', 'revelation', 'praise', 'completion'
    expects_response: bool = False


class LessonSessionResponse(BaseModel):
    """Lesson session response"""
    id: UUID
    lesson_id: UUID
    user_id: UUID
    status: str  # 'in_progress', 'completed', 'abandoned'
    started_at: datetime

    class Config:
        from_attributes = True


# Request models
class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    session_id: UUID
    message: str
    action_type: str = "text_response"


class ActionRequest(BaseModel):
    """Request model for action endpoint"""
    session_id: UUID
    action: Dict[str, Any]  # Flexible action structure


class CombineBlocksRequest(BaseModel):
    """Request model for combine-blocks endpoint"""
    session_id: UUID
    block_ids: List[str]


class QuestionRequest(BaseModel):
    """Request model for question endpoint"""
    session_id: UUID


class AnswerRequest(BaseModel):
    """Request model for answer endpoint"""
    session_id: UUID
    question_id: str
    answer: str


class CompleteRequest(BaseModel):
    """Request model for complete endpoint"""
    session_id: UUID


# Response models for specific endpoints
class LessonDataResponse(BaseModel):
    """Response for GET /lessons/fractions"""
    lesson: LessonResponse
    manipulative_state: ManipulativeStateResponse


class StartLessonResponse(BaseModel):
    """Response for POST /lessons/fractions/start"""
    lesson_session: LessonSessionResponse
    tutor_message: TutorMessageResponse


class ChatResponse(BaseModel):
    """Response for POST /lessons/fractions/chat"""
    tutor_message: TutorMessageResponse


class ActionResponse(BaseModel):
    """Response for POST /lessons/fractions/action"""
    manipulative_state: ManipulativeStateResponse
    tutor_message: TutorMessageResponse


class CombineBlocksResponse(BaseModel):
    """Response for POST /lessons/fractions/combine-blocks"""
    manipulative_state: ManipulativeStateResponse
    tutor_message: TutorMessageResponse


class QuestionResponse(BaseModel):
    """Response for POST /lessons/fractions/question"""
    question: Dict[str, Any]  # Flexible question structure


class AnswerResponse(BaseModel):
    """Response for POST /lessons/fractions/answer"""
    is_correct: bool
    tutor_message: TutorMessageResponse
    next_question: Optional[Dict[str, Any]] = None


class ProgressResponse(BaseModel):
    """Response for GET /lessons/fractions/progress"""
    session: Dict[str, Any]  # Session with progress data
    achievements: List[Dict[str, Any]] = []


class CompletionResponse(BaseModel):
    """Response for POST /lessons/fractions/complete"""
    completion: Dict[str, Any]
    tutor_message: TutorMessageResponse
