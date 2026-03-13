"""
Lesson endpoints
"""
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.services.lesson_service import (
    get_lesson_data,
    start_lesson,
    handle_chat,
    handle_action,
    handle_combine_blocks,
    get_question,
    handle_answer,
    get_progress_for_user,
    complete_lesson
)
from app.models.common import StandardResponse
from app.models.lesson import (
    LessonDataResponse,
    ChatRequest,
    ActionRequest,
    CombineBlocksRequest,
    QuestionRequest,
    AnswerRequest,
    CompleteRequest
)
from models.user import User

router = APIRouter(prefix="/lessons/fractions", tags=["lessons"])


@router.get("", response_model=StandardResponse)
async def get_lessons_fractions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the fraction equivalence lesson data and initial state"""
    try:
        lesson_data = get_lesson_data(db, current_user.id)
        return StandardResponse(data=lesson_data.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.post("/start", response_model=StandardResponse)
async def start_lessons_fractions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start the fraction lesson and get the first tutor message"""
    try:
        start_response = start_lesson(db, current_user.id)
        return StandardResponse(data=start_response.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.post("/chat", response_model=StandardResponse)
async def chat_lessons_fractions(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send student response or get next tutor message based on current lesson state"""
    try:
        chat_response = handle_chat(db, request.session_id, current_user.id, request.message)
        return StandardResponse(data=chat_response.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.post("/action", response_model=StandardResponse)
async def action_lessons_fractions(
    request: ActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record student action with the manipulative and get tutor response"""
    try:
        action_response = handle_action(db, request.session_id, current_user.id, request.action)
        return StandardResponse(data=action_response.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.post("/combine-blocks", response_model=StandardResponse)
async def combine_blocks_lessons_fractions(
    request: CombineBlocksRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Combine fraction blocks when student performs combination action"""
    try:
        combine_response = handle_combine_blocks(db, request.session_id, current_user.id, request.block_ids)
        return StandardResponse(data=combine_response.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.post("/question", response_model=StandardResponse)
async def question_lessons_fractions(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a check-for-understanding question"""
    try:
        question_response = get_question(db, request.session_id, current_user.id)
        return StandardResponse(data=question_response.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.post("/answer", response_model=StandardResponse)
async def answer_lessons_fractions(
    request: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit answer to assessment question"""
    try:
        answer_response = handle_answer(db, request.session_id, current_user.id, request.question_id, request.answer)
        return StandardResponse(data=answer_response.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.get("/progress", response_model=StandardResponse)
async def progress_lessons_fractions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current lesson progress and completion status"""
    try:
        progress_response = get_progress_for_user(db, current_user.id)
        return StandardResponse(data=progress_response.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.post("/complete", response_model=StandardResponse)
async def complete_lessons_fractions(
    request: CompleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark lesson as completed when student finishes all assessment questions"""
    try:
        complete_response = complete_lesson(db, request.session_id, current_user.id)
        return StandardResponse(data=complete_response.model_dump(), error=None)
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )
