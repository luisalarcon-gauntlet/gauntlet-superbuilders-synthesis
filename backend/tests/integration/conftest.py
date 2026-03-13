"""
Pytest configuration for integration tests

Integration tests require:
1. A running database (PostgreSQL)
2. A running FastAPI server (uvicorn app.main:app)
3. Database migrations applied
4. Seed data available

Setup:
1. Start database: docker-compose up -d db
2. Run migrations: cd backend && python run_migrations.py
3. Start server: cd backend && uvicorn app.main:app --reload
4. Run tests: pytest backend/tests/integration/
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from config import DATABASE_URL
from models.lesson import Lesson
from models.lesson_step import LessonStep
import uuid
from datetime import datetime, timezone


# Use the same database connection as the app
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_lesson_data(db):
    """Seed lesson data for integration tests"""
    # Check if lesson already exists
    existing_lesson = db.query(Lesson).filter(Lesson.topic == "fractions").first()
    if existing_lesson:
        return existing_lesson
    
    # Create lesson
    lesson = Lesson(
        id=uuid.UUID('22222222-2222-2222-2222-222222222222'),
        title="Fraction Equivalence",
        description="Learn that 1/2 equals 2/4 through interactive exploration",
        topic="fractions",
        difficulty_level=3,
        is_active=True
    )
    db.add(lesson)
    db.flush()
    
    # Create lesson steps
    steps_data = [
        {
            "step_number": 1,
            "step_type": "introduction",
            "tutor_message": "Welcome! Today we're going to explore fractions. Can you see the fraction blocks on your screen?",
            "expected_action": "Look at the manipulatives",
            "success_message": "Great! You're ready to explore!",
            "hint_message": "Take a look at the colorful blocks on your screen."
        },
        {
            "step_number": 2,
            "step_type": "exploration",
            "tutor_message": "Try dragging a fraction block into the workspace. What do you notice?",
            "expected_action": "Place a block",
            "success_message": "Excellent! You're exploring the fractions!",
            "hint_message": "Click and drag a block to move it."
        },
        {
            "step_number": 3,
            "step_type": "guided_discovery",
            "tutor_message": "Now try combining two 1/4 blocks. What do you think they equal?",
            "expected_action": "Combine blocks",
            "success_message": "Wonderful discovery! Two 1/4 blocks equal 1/2!",
            "hint_message": "Drag two blocks close together to combine them."
        },
        {
            "step_number": 4,
            "step_type": "assessment",
            "tutor_message": "Let's check your understanding. Which fraction is equivalent to 1/2?",
            "expected_action": "Answer question",
            "success_message": "Perfect! You understand fraction equivalence!",
            "hint_message": "Think about what we discovered with the blocks."
        },
        {
            "step_number": 5,
            "step_type": "completion",
            "tutor_message": "Congratulations! You've completed the lesson on fraction equivalence!",
            "expected_action": "Complete lesson",
            "success_message": "Well done! You've mastered fraction equivalence!",
            "hint_message": "You're all done!"
        }
    ]
    
    for step_data in steps_data:
        step = LessonStep(
            id=uuid.uuid4(),
            lesson_id=lesson.id,
            **step_data
        )
        db.add(step)
    
    db.commit()
    return lesson


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each integration test"""
    # Don't drop/create tables - use existing database
    # Integration tests run against the actual database
    db = TestingSessionLocal()
    try:
        # Seed lesson data if needed
        seed_lesson_data(db)
        yield db
    finally:
        db.rollback()  # Rollback any changes made during test
        db.close()
