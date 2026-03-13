"""
Seed script for minimal happy path testing data.

Creates:
- Test User: "Test Student"
- Fraction Equivalence Lesson with 8-10 steps
- Sample in-progress session
- Sample manipulative interactions
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import uuid
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)
else:
    # Try alternative path (when running from container)
    sys.path.insert(0, '/app')

from backend.config import settings
from backend.models.user import User
from backend.models.lesson import Lesson
from backend.models.lesson_step import LessonStep
from backend.models.user_session import UserSession
from backend.models.manipulative_interaction import ManipulativeInteraction
from backend.models.conversation_log import ConversationLog


def seed_user(session):
    """Create test user if it doesn't exist"""
    existing_user = session.query(User).filter(User.name == "Test Student").first()
    
    if existing_user:
        print("✓ Test Student already exists")
        return existing_user
    
    user = User(
        id=uuid.UUID('11111111-1111-1111-1111-111111111111'),
        name="Test Student",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(user)
    print("✓ Created Test Student")
    return user


def seed_lesson(session):
    """Create fraction equivalence lesson if it doesn't exist"""
    existing_lesson = session.query(Lesson).filter(Lesson.topic == "fractions").first()
    
    if existing_lesson:
        print("✓ Fraction Equivalence lesson already exists")
        return existing_lesson
    
    lesson = Lesson(
        id=uuid.UUID('22222222-2222-2222-2222-222222222222'),
        title="Fraction Equivalence",
        description="Learn that 1/2 equals 2/4 through interactive exploration",
        topic="fractions",
        difficulty_level=3,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(lesson)
    print("✓ Created Fraction Equivalence lesson")
    return lesson


def seed_lesson_steps(session, lesson):
    """Create lesson steps for fraction equivalence lesson"""
    existing_steps = session.query(LessonStep).filter(LessonStep.lesson_id == lesson.id).count()
    
    if existing_steps > 0:
        print(f"✓ Lesson steps already exist ({existing_steps} steps)")
        return session.query(LessonStep).filter(LessonStep.lesson_id == lesson.id).order_by(LessonStep.step_number).all()
    
    steps_data = [
        {
            "step_number": 1,
            "step_type": "exploration",
            "tutor_message": "Welcome! Today we're going to explore fractions. Let's start by looking at some fraction blocks. Can you see the 1/2 block?",
            "expected_action": "Identify 1/2 block",
            "success_message": "Great! You found the 1/2 block!",
            "hint_message": "Look for a block that's divided into 2 equal parts, with 1 part colored."
        },
        {
            "step_number": 2,
            "step_type": "instruction",
            "tutor_message": "Now let's look at the 2/4 block. Notice how it's divided into 4 equal parts, with 2 parts colored.",
            "expected_action": "Observe 2/4 block",
            "success_message": "Perfect observation!",
            "hint_message": "The 2/4 block has 4 equal parts total, and 2 of them are colored."
        },
        {
            "step_number": 3,
            "step_type": "question",
            "tutor_message": "What do you notice about the 1/2 block and the 2/4 block? Do they look the same size?",
            "expected_action": "Compare blocks visually",
            "success_message": "Excellent! They are the same size!",
            "hint_message": "Try placing them side by side. Do they cover the same amount of space?"
        },
        {
            "step_number": 4,
            "step_type": "exploration",
            "tutor_message": "Try dragging the 1/2 block and the 2/4 block next to each other. What happens?",
            "expected_action": "Drag blocks together",
            "success_message": "Wonderful! They match up perfectly!",
            "hint_message": "Drag one block close to the other and see if they align."
        },
        {
            "step_number": 5,
            "step_type": "question",
            "tutor_message": "If 1/2 and 2/4 are the same size, what does that tell us about these fractions?",
            "expected_action": "Recognize equivalence",
            "success_message": "Yes! 1/2 equals 2/4! They are equivalent fractions!",
            "hint_message": "Think about what 'equal' means. If they're the same size, they represent the same amount."
        },
        {
            "step_number": 6,
            "step_type": "instruction",
            "tutor_message": "Fractions that represent the same amount are called 'equivalent fractions'. 1/2 and 2/4 are equivalent because they cover the same space.",
            "expected_action": "Understand concept",
            "success_message": "You're getting it!",
            "hint_message": "Remember: equivalent means 'equal in value'."
        },
        {
            "step_number": 7,
            "step_type": "question",
            "tutor_message": "Can you find another fraction that might be equivalent to 1/2? Try exploring with the blocks!",
            "expected_action": "Find equivalent fraction",
            "success_message": "Great discovery! Fractions like 3/6 or 4/8 are also equivalent to 1/2!",
            "hint_message": "Look for blocks that are the same size as the 1/2 block."
        },
        {
            "step_number": 8,
            "step_type": "check",
            "tutor_message": "Let's check your understanding. Can you combine blocks to show that 1/2 equals 2/4?",
            "expected_action": "Combine blocks to demonstrate equivalence",
            "success_message": "Perfect! You've shown that 1/2 equals 2/4!",
            "hint_message": "Try placing the 1/2 block and 2/4 block together to show they're the same."
        },
        {
            "step_number": 9,
            "step_type": "instruction",
            "tutor_message": "Excellent work! You've learned that different fractions can represent the same amount. This is called fraction equivalence.",
            "expected_action": None,
            "success_message": "You're doing great!",
            "hint_message": None
        },
        {
            "step_number": 10,
            "step_type": "check",
            "tutor_message": "Final check: Can you tell me in your own words what equivalent fractions are?",
            "expected_action": "Explain concept",
            "success_message": "Perfect explanation! You understand equivalent fractions!",
            "hint_message": "Think about what makes fractions equivalent - they represent the same amount."
        }
    ]
    
    steps = []
    for i, step_data in enumerate(steps_data):
        step = LessonStep(
            id=uuid.UUID(f'33333333-3333-3333-3333-{str(i+1).zfill(12)}'),
            lesson_id=lesson.id,
            step_number=step_data["step_number"],
            step_type=step_data["step_type"],
            tutor_message=step_data["tutor_message"],
            expected_action=step_data["expected_action"],
            success_message=step_data["success_message"],
            hint_message=step_data["hint_message"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        session.add(step)
        steps.append(step)
    
    print(f"✓ Created {len(steps)} lesson steps")
    return steps


def seed_session(session, user, lesson, steps):
    """Create sample in-progress session"""
    existing_session = session.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.lesson_id == lesson.id,
        UserSession.status == "in_progress"
    ).first()
    
    if existing_session:
        print("✓ Sample session already exists")
        return existing_session
    
    session_obj = UserSession(
        id=uuid.UUID('44444444-4444-4444-4444-444444444444'),
        user_id=user.id,
        lesson_id=lesson.id,
        status="in_progress",
        current_step_id=steps[2].id,  # Currently on step 3
        started_at=datetime.now(timezone.utc),
        completed_at=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(session_obj)
    print("✓ Created sample in-progress session")
    return session_obj


def seed_interactions(session, session_obj, steps):
    """Create sample manipulative interactions"""
    existing_interactions = session.query(ManipulativeInteraction).filter(
        ManipulativeInteraction.session_id == session_obj.id
    ).count()
    
    if existing_interactions > 0:
        print(f"✓ Sample interactions already exist ({existing_interactions} interactions)")
        return
    
    interactions_data = [
        {
            "step_id": steps[0].id,
            "interaction_type": "drag",
            "fraction_value": "1/2",
            "position_x": 100,
            "position_y": 150,
            "is_correct": True,
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "step_id": steps[1].id,
            "interaction_type": "drag",
            "fraction_value": "2/4",
            "position_x": 200,
            "position_y": 150,
            "is_correct": True,
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "step_id": steps[3].id,
            "interaction_type": "combine",
            "fraction_value": "1/2",
            "position_x": 150,
            "position_y": 150,
            "is_correct": True,
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "step_id": steps[3].id,
            "interaction_type": "compare",
            "fraction_value": "2/4",
            "position_x": 150,
            "position_y": 150,
            "is_correct": True,
            "timestamp": datetime.now(timezone.utc)
        }
    ]
    
    for i, interaction_data in enumerate(interactions_data):
        interaction = ManipulativeInteraction(
            id=uuid.UUID(f'55555555-5555-5555-5555-{str(i+1).zfill(12)}'),
            session_id=session_obj.id,
            step_id=interaction_data["step_id"],
            interaction_type=interaction_data["interaction_type"],
            fraction_value=interaction_data["fraction_value"],
            position_x=interaction_data["position_x"],
            position_y=interaction_data["position_y"],
            is_correct=interaction_data["is_correct"],
            timestamp=interaction_data["timestamp"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        session.add(interaction)
    
    print(f"✓ Created {len(interactions_data)} sample interactions")


def main():
    """Run all seed functions"""
    print("Starting seed data creation...")
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    
    with SessionLocal() as session:
        try:
            user = seed_user(session)
            lesson = seed_lesson(session)
            steps = seed_lesson_steps(session, lesson)
            session_obj = seed_session(session, user, lesson, steps)
            seed_interactions(session, session_obj, steps)
            
            session.commit()
            print("\n✓ All seeds completed successfully!")
        except Exception as e:
            session.rollback()
            print(f"\n✗ Error seeding data: {e}")
            raise


if __name__ == "__main__":
    main()
