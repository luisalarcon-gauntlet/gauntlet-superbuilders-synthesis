"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, engine
from models.base import Base
from config import DATABASE_URL
from models.lesson import Lesson
from models.lesson_step import LessonStep
import uuid
from datetime import datetime, timezone

# Use the same database connection as the app
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_lesson_data(db):
    """Seed lesson data for tests"""
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
    
    # Create first step
    step = LessonStep(
        id=uuid.UUID('33333333-3333-3333-3333-333333333333'),
        lesson_id=lesson.id,
        step_number=1,
        step_type="exploration",
        tutor_message="Welcome! Today we're going to explore fractions. Can you see the fraction blocks on your screen?",
        expected_action="Look at the manipulatives",
        success_message="Great! You're ready to explore!",
        hint_message="Take a look at the colorful blocks on your screen."
    )
    db.add(step)
    db.commit()
    return lesson


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        # Seed lesson data
        seed_lesson_data(db)
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
