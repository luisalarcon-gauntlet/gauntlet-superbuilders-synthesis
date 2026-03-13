"""
Lesson service - business logic for lesson operations
"""
from sqlalchemy.orm import Session
from models.lesson import Lesson
from models.lesson_step import LessonStep
from models.user_session import UserSession
from models.conversation_log import ConversationLog
from models.manipulative_interaction import ManipulativeInteraction
from app.models.lesson import (
    LessonResponse,
    LessonDataResponse,
    ManipulativeStateResponse,
    BlockModel,
    WorkspaceModel,
    StartLessonResponse,
    LessonSessionResponse,
    TutorMessageResponse,
    ChatResponse,
    ActionResponse,
    CombineBlocksResponse,
    QuestionResponse,
    AnswerResponse,
    ProgressResponse,
    CompletionResponse
)
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime, timezone
from typing import Dict, Any, List


def get_fraction_lesson(db: Session) -> Lesson:
    """Get the fraction equivalence lesson"""
    lesson = db.query(Lesson).filter(
        Lesson.topic == "fractions",
        Lesson.is_active == True
    ).first()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fraction lesson not found"
        )
    
    return lesson


def get_lesson_status_for_user(db: Session, user_id: UUID, lesson_id: UUID) -> str:
    """Get lesson status for a user: 'not_started', 'in_progress', or 'completed'"""
    session = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.lesson_id == lesson_id
    ).order_by(UserSession.started_at.desc()).first()
    
    if not session:
        return "not_started"
    
    if session.status == "completed":
        return "completed"
    elif session.status == "in_progress":
        return "in_progress"
    else:
        return "not_started"


def get_initial_manipulative_state() -> ManipulativeStateResponse:
    """Get initial manipulative state with available blocks"""
    available_blocks = [
        BlockModel(
            id="half_1",
            type="1/2",
            position=None,
            color="#FF6B6B"
        ),
        BlockModel(
            id="quarter_1",
            type="1/4",
            position=None,
            color="#4ECDC4"
        ),
        BlockModel(
            id="quarter_2",
            type="1/4",
            position=None,
            color="#4ECDC4"
        )
    ]
    
    workspace = WorkspaceModel(
        width=800,
        height=400,
        placed_blocks=[]
    )
    
    return ManipulativeStateResponse(
        available_blocks=available_blocks,
        workspace=workspace
    )


def get_lesson_data(db: Session, user_id: UUID) -> LessonDataResponse:
    """Get lesson data and initial manipulative state"""
    lesson = get_fraction_lesson(db)
    status = get_lesson_status_for_user(db, user_id, lesson.id)
    
    lesson_response = LessonResponse(
        id=lesson.id,
        title=lesson.title,
        description=lesson.description or "",
        status=status
    )
    
    manipulative_state = get_initial_manipulative_state()
    
    return LessonDataResponse(
        lesson=lesson_response,
        manipulative_state=manipulative_state
    )


def start_lesson(db: Session, user_id: UUID) -> StartLessonResponse:
    """Start a lesson session and return first tutor message"""
    lesson = get_fraction_lesson(db)
    
    # Check if there's an existing in-progress session
    existing_session = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.lesson_id == lesson.id,
        UserSession.status == "in_progress"
    ).first()
    
    if existing_session:
        # Return existing session
        session = existing_session
    else:
        # Get first step
        first_step = db.query(LessonStep).filter(
            LessonStep.lesson_id == lesson.id
        ).order_by(LessonStep.step_number).first()
        
        if not first_step:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson has no steps"
            )
        
        # Create new session
        session = UserSession(
            user_id=user_id,
            lesson_id=lesson.id,
            status="in_progress",
            current_step_id=first_step.id,
            started_at=datetime.now(timezone.utc)
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # Get current step
    current_step = db.query(LessonStep).filter(
        LessonStep.id == session.current_step_id
    ).first() if session.current_step_id else None
    
    if not current_step:
        # Get first step if no current step
        current_step = db.query(LessonStep).filter(
            LessonStep.lesson_id == lesson.id
        ).order_by(LessonStep.step_number).first()
    
    # Create tutor message from step
    tutor_message = TutorMessageResponse(
        id=f"msg_{current_step.step_number}",
        text=current_step.tutor_message,
        type=current_step.step_type,
        expects_response=False
    )
    
    # Create session response
    session_response = LessonSessionResponse(
        id=session.id,
        lesson_id=session.lesson_id,
        user_id=session.user_id,
        status=session.status,
        started_at=session.started_at
    )
    
    return StartLessonResponse(
        lesson_session=session_response,
        tutor_message=tutor_message
    )


def get_session(db: Session, session_id: UUID, user_id: UUID) -> UserSession:
    """Get and validate a user session"""
    session = db.query(UserSession).filter(
        UserSession.id == session_id,
        UserSession.user_id == user_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


def get_current_step(db: Session, session: UserSession) -> LessonStep:
    """Get current step for a session"""
    if not session.current_step_id:
        # Get first step if no current step
        lesson = get_fraction_lesson(db)
        step = db.query(LessonStep).filter(
            LessonStep.lesson_id == lesson.id
        ).order_by(LessonStep.step_number).first()
    else:
        step = db.query(LessonStep).filter(
            LessonStep.id == session.current_step_id
        ).first()
    
    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Step not found"
        )
    
    return step


def advance_to_next_step(db: Session, session: UserSession) -> LessonStep:
    """Advance session to next step"""
    current_step = get_current_step(db, session)
    
    # Get next step
    next_step = db.query(LessonStep).filter(
        LessonStep.lesson_id == session.lesson_id,
        LessonStep.step_number > current_step.step_number
    ).order_by(LessonStep.step_number).first()
    
    if next_step:
        session.current_step_id = next_step.id
        db.commit()
        db.refresh(session)
        return next_step
    else:
        # No more steps - lesson complete
        return current_step


def handle_chat(db: Session, session_id: UUID, user_id: UUID, message: str) -> ChatResponse:
    """Handle chat message and return tutor response"""
    session = get_session(db, session_id, user_id)
    current_step = get_current_step(db, session)
    
    # Log student message
    conversation_log = ConversationLog(
        session_id=session.id,
        step_id=current_step.id,
        speaker="student",
        message=message,
        message_type="response",
        timestamp=datetime.now(timezone.utc)
    )
    db.add(conversation_log)
    
    # Advance to next step and get tutor message
    next_step = advance_to_next_step(db, session)
    
    # Log tutor response
    tutor_log = ConversationLog(
        session_id=session.id,
        step_id=next_step.id,
        speaker="tutor",
        message=next_step.tutor_message,
        message_type=next_step.step_type,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(tutor_log)
    db.commit()
    
    tutor_message = TutorMessageResponse(
        id=f"msg_{next_step.step_number}",
        text=next_step.tutor_message,
        type=next_step.step_type,
        expects_response=False
    )
    
    return ChatResponse(tutor_message=tutor_message)


def handle_action(db: Session, session_id: UUID, user_id: UUID, action: Dict[str, Any]) -> ActionResponse:
    """Handle manipulative action and return tutor response"""
    session = get_session(db, session_id, user_id)
    current_step = get_current_step(db, session)
    
    # Extract action data
    action_type = action.get("type", "place_block")
    block_id = action.get("block_id")
    position = action.get("position", {})
    
    # Determine fraction value from block_id
    fraction_value = "1/2" if "half" in block_id else "1/4" if "quarter" in block_id else "1/2"
    
    # Log interaction
    interaction = ManipulativeInteraction(
        session_id=session.id,
        step_id=current_step.id,
        interaction_type=action_type,
        fraction_value=fraction_value,
        position_x=position.get("x"),
        position_y=position.get("y"),
        is_correct=True,  # Happy path - assume correct
        timestamp=datetime.now(timezone.utc)
    )
    db.add(interaction)
    
    # Create updated manipulative state
    placed_block = BlockModel(
        id=block_id,
        type=fraction_value,
        position=position,
        color="#FF6B6B" if "half" in block_id else "#4ECDC4"
    )
    
    manipulative_state = ManipulativeStateResponse(
        available_blocks=[],
        workspace=WorkspaceModel(
            width=800,
            height=400,
            placed_blocks=[placed_block]
        )
    )
    
    # Get tutor message
    tutor_message = TutorMessageResponse(
        id=f"msg_{current_step.step_number}",
        text=current_step.success_message or current_step.tutor_message,
        type="encouragement",
        expects_response=False
    )
    
    db.commit()
    
    return ActionResponse(
        manipulative_state=manipulative_state,
        tutor_message=tutor_message
    )


def handle_combine_blocks(db: Session, session_id: UUID, user_id: UUID, block_ids: List[str]) -> CombineBlocksResponse:
    """Handle block combination and return tutor response"""
    session = get_session(db, session_id, user_id)
    current_step = get_current_step(db, session)
    
    # Log combination interaction
    interaction = ManipulativeInteraction(
        session_id=session.id,
        step_id=current_step.id,
        interaction_type="combine",
        fraction_value="2/4",
        position_x=100,
        position_y=200,
        is_correct=True,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(interaction)
    
    # Create combined block
    combined_block = BlockModel(
        id="combined_half",
        type="2/4",
        display="1/2",
        position={"x": 100, "y": 200},
        color="#4ECDC4",
        is_combined=True
    )
    
    manipulative_state = ManipulativeStateResponse(
        available_blocks=[],
        workspace=WorkspaceModel(
            width=800,
            height=400,
            placed_blocks=[combined_block]
        )
    )
    
    # Create revelation message
    tutor_message = TutorMessageResponse(
        id=f"msg_{current_step.step_number}",
        text="Wow! Look what happened! When you put those two 1/4 blocks together, they make the same size as the 1/2 block. This means 2/4 equals 1/2! They're equivalent fractions.",
        type="revelation",
        expects_response=False
    )
    
    db.commit()
    
    return CombineBlocksResponse(
        manipulative_state=manipulative_state,
        tutor_message=tutor_message
    )


def get_question(db: Session, session_id: UUID, user_id: UUID) -> QuestionResponse:
    """Get a check-for-understanding question"""
    session = get_session(db, session_id, user_id)
    current_step = get_current_step(db, session)
    
    # Create question based on step
    question = {
        "id": f"q{current_step.step_number}",
        "text": "Which fraction is equivalent to 1/2?",
        "type": "multiple_choice",
        "options": ["1/4", "2/4", "3/4", "4/4"],
        "correct_answer": "2/4"
    }
    
    return QuestionResponse(question=question)


def handle_answer(db: Session, session_id: UUID, user_id: UUID, question_id: str, answer: str) -> AnswerResponse:
    """Handle answer submission and return tutor response"""
    session = get_session(db, session_id, user_id)
    current_step = get_current_step(db, session)
    
    # Simple check - in happy path, assume correct if answer is "2/4"
    is_correct = answer == "2/4"
    
    # Create tutor message
    if is_correct:
        tutor_message = TutorMessageResponse(
            id=f"msg_{current_step.step_number}",
            text="Excellent! You're absolutely right. 2/4 is equivalent to 1/2. You really understand this concept!",
            type="praise",
            expects_response=False
        )
    else:
        tutor_message = TutorMessageResponse(
            id=f"msg_{current_step.step_number}",
            text="Good try! Let's think about this again. Remember that equivalent fractions are the same size.",
            type="encouragement",
            expects_response=False
        )
    
    # Create next question (if not last)
    next_step = db.query(LessonStep).filter(
        LessonStep.lesson_id == session.lesson_id,
        LessonStep.step_number > current_step.step_number
    ).order_by(LessonStep.step_number).first()
    
    next_question = None
    if next_step and next_step.step_type == "question":
        next_question = {
            "id": f"q{next_step.step_number}",
            "text": "Now try this one: Which two fractions shown below are equivalent?",
            "type": "visual_comparison",
            "fraction_pairs": [["1/3", "2/6"], ["1/4", "3/8"], ["2/3", "4/6"]]
        }
    
    return AnswerResponse(
        is_correct=is_correct,
        tutor_message=tutor_message,
        next_question=next_question
    )


def get_progress_for_user(db: Session, user_id: UUID) -> ProgressResponse:
    """Get lesson progress for user's active session"""
    lesson = get_fraction_lesson(db)
    session = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.lesson_id == lesson.id
    ).order_by(UserSession.started_at.desc()).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active session found"
        )
    
    return get_progress(db, session.id, user_id)


def get_progress(db: Session, session_id: UUID, user_id: UUID) -> ProgressResponse:
    """Get lesson progress and completion status"""
    session = get_session(db, session_id, user_id)
    lesson = get_fraction_lesson(db)
    
    # Count total steps
    total_steps = db.query(LessonStep).filter(
        LessonStep.lesson_id == lesson.id
    ).count()
    
    # Calculate progress
    current_step = get_current_step(db, session)
    progress_percentage = int((current_step.step_number / total_steps) * 100) if total_steps > 0 else 0
    
    # Count questions answered (simplified - count interactions)
    questions_answered = db.query(ManipulativeInteraction).filter(
        ManipulativeInteraction.session_id == session.id
    ).count()
    
    # Count correct answers (simplified - assume all correct in happy path)
    correct_answers = questions_answered
    
    session_data = {
        "id": str(session.id),
        "status": session.status,
        "progress_percentage": progress_percentage,
        "questions_answered": questions_answered,
        "correct_answers": correct_answers,
        "completed_at": session.completed_at.isoformat() if session.completed_at else None
    }
    
    # Simple achievements (happy path)
    achievements = []
    if questions_answered > 0:
        achievements.append({
            "title": "Fraction Explorer",
            "description": "Successfully combined fraction blocks",
            "earned_at": session.started_at.isoformat()
        })
    if session.status == "completed":
        achievements.append({
            "title": "Equivalence Expert",
            "description": "Completed lesson with 100% accuracy",
            "earned_at": session.completed_at.isoformat() if session.completed_at else session.started_at.isoformat()
        })
    
    return ProgressResponse(
        session=session_data,
        achievements=achievements
    )


def complete_lesson(db: Session, session_id: UUID, user_id: UUID) -> CompletionResponse:
    """Mark lesson as completed"""
    session = get_session(db, session_id, user_id)
    
    # Mark as completed
    session.status = "completed"
    session.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    
    # Calculate completion metrics
    lesson = get_fraction_lesson(db)
    total_steps = db.query(LessonStep).filter(
        LessonStep.lesson_id == lesson.id
    ).count()
    
    # Calculate time (simplified)
    time_diff = session.completed_at - session.started_at
    completion_time = f"{int(time_diff.total_seconds() / 60)} minutes"
    
    completion_data = {
        "lesson_completed": True,
        "completion_time": completion_time,
        "final_score": 100,  # Happy path - assume perfect score
        "mastery_level": "excellent"
    }
    
    tutor_message = TutorMessageResponse(
        id="msg_final",
        text="Congratulations! You've mastered fraction equivalence. You discovered that fractions like 1/2 and 2/4 represent the same amount, just divided into different pieces. Great work today!",
        type="completion",
        expects_response=False
    )
    
    return CompletionResponse(
        completion=completion_data,
        tutor_message=tutor_message
    )
