"""
Seed script for minimal happy path testing data
"""
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
import uuid

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from backend.config import DATABASE_URL
    from backend.models import User, Lesson, LessonStep, UserSession, ManipulativeInteraction, ConversationLog
except ImportError:
    from config import DATABASE_URL
    from models import User, Lesson, LessonStep, UserSession, ManipulativeInteraction, ConversationLog


def seed_user(session):
    """Seed test user"""
    existing_user = session.query(User).filter(User.name == "Test Student").first()
    
    if not existing_user:
        user = User(
            id=uuid.UUID('11111111-1111-1111-1111-111111111111'),
            name="Test Student"
        )
        session.add(user)
        print("✓ Created test user: Test Student")
        return user
    else:
        print("✓ Test user already exists")
        return existing_user


def seed_lesson(session):
    """Seed fraction equivalence lesson with steps"""
    existing_lesson = session.query(Lesson).filter(Lesson.title == "Fraction Equivalence").first()
    
    if existing_lesson:
        print("✓ Fraction equivalence lesson already exists")
        return existing_lesson
    
    lesson = Lesson(
        id=uuid.UUID('22222222-2222-2222-2222-222222222222'),
        title="Fraction Equivalence",
        description="Learn that 1/2 equals 2/4 through interactive exploration",
        topic="fractions",
        difficulty_level=3,
        is_active=True
    )
    session.add(lesson)
    session.flush()  # Flush to get lesson.id
    
    # Create lesson steps
    steps_data = [
        {
            "step_number": 1,
            "step_type": "exploration",
            "tutor_message": "Welcome! Today we're going to explore fractions. Can you see the fraction blocks on your screen?",
            "expected_action": "Look at the manipulatives",
            "success_message": "Great! You're ready to explore!",
            "hint_message": "Take a look at the colorful blocks on your screen."
        },
        {
            "step_number": 2,
            "step_type": "instruction",
            "tutor_message": "Let's start with 1/2. Drag a 1/2 block onto the workspace.",
            "expected_action": "Drag 1/2 block",
            "success_message": "Perfect! You've placed 1/2 on the workspace.",
            "hint_message": "Click and drag the block that shows one half."
        },
        {
            "step_number": 3,
            "step_type": "exploration",
            "tutor_message": "Now, can you find blocks that look the same size as 1/2? Try dragging a 2/4 block next to it.",
            "expected_action": "Drag 2/4 block next to 1/2",
            "success_message": "Excellent! You found that 2/4 is the same size as 1/2!",
            "hint_message": "Look for blocks that cover the same amount of space."
        },
        {
            "step_number": 4,
            "step_type": "question",
            "tutor_message": "What do you notice about 1/2 and 2/4? Are they the same size?",
            "expected_action": "Compare the blocks",
            "success_message": "That's right! They are the same size!",
            "hint_message": "Look carefully at how much space each block covers."
        },
        {
            "step_number": 5,
            "step_type": "instruction",
            "tutor_message": "When two fractions are the same size, we say they are equivalent. 1/2 and 2/4 are equivalent fractions!",
            "expected_action": "Listen to explanation",
            "success_message": "You're learning about equivalent fractions!",
            "hint_message": "Remember: equivalent means the same value."
        },
        {
            "step_number": 6,
            "step_type": "exploration",
            "tutor_message": "Let's try another one! Can you find a fraction equivalent to 1/3? Try combining smaller pieces.",
            "expected_action": "Find equivalent to 1/3",
            "success_message": "Great thinking! You're exploring fractions!",
            "hint_message": "Try combining pieces to make the same size as 1/3."
        },
        {
            "step_number": 7,
            "step_type": "question",
            "tutor_message": "If you have 2/6, is that the same as 1/3? Drag them together to check!",
            "expected_action": "Compare 2/6 and 1/3",
            "success_message": "Yes! 2/6 equals 1/3. You're getting it!",
            "hint_message": "Place them side by side and see if they match."
        },
        {
            "step_number": 8,
            "step_type": "check",
            "tutor_message": "Let's check what you've learned! Which fraction is equivalent to 1/2: 2/4, 3/6, or 4/8?",
            "expected_action": "Select equivalent fraction",
            "success_message": "All of them! 1/2 = 2/4 = 3/6 = 4/8. You're a fraction expert!",
            "hint_message": "Remember: equivalent fractions are the same size, just divided differently."
        }
    ]
    
    steps = []
    for i, step_data in enumerate(steps_data):
        step = LessonStep(
            id=uuid.UUID(f'33333333-3333-3333-3333-{str(i+1).zfill(12)}'),
            lesson_id=lesson.id,
            **step_data
        )
        session.add(step)
        steps.append(step)
    
    print(f"✓ Created fraction equivalence lesson with {len(steps)} steps")
    return lesson, steps


def seed_session(session, user, lesson, steps):
    """Seed sample in-progress session"""
    existing_session = session.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.lesson_id == lesson.id,
        UserSession.status == 'in_progress'
    ).first()
    
    if existing_session:
        print("✓ Sample session already exists")
        return existing_session
    
    user_session = UserSession(
        id=uuid.UUID('44444444-4444-4444-4444-444444444444'),
        user_id=user.id,
        lesson_id=lesson.id,
        status='in_progress',
        current_step_id=steps[2].id,  # On step 3
        started_at=datetime.now(timezone.utc)
    )
    session.add(user_session)
    session.flush()
    
    print("✓ Created sample in-progress session")
    return user_session


def seed_interactions(session, user_session, steps):
    """Seed sample manipulative interactions"""
    existing_interactions = session.query(ManipulativeInteraction).filter(
        ManipulativeInteraction.session_id == user_session.id
    ).first()
    
    if existing_interactions:
        print("✓ Sample interactions already exist")
        return
    
    interactions_data = [
        {
            "step_id": steps[1].id,  # Step 2: Drag 1/2
            "interaction_type": "drag",
            "fraction_value": "1/2",
            "position_x": 100,
            "position_y": 150,
            "is_correct": True,
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "step_id": steps[2].id,  # Step 3: Drag 2/4
            "interaction_type": "drag",
            "fraction_value": "2/4",
            "position_x": 300,
            "position_y": 150,
            "is_correct": True,
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "step_id": steps[2].id,  # Step 3: Compare
            "interaction_type": "compare",
            "fraction_value": "1/2,2/4",
            "position_x": 200,
            "position_y": 150,
            "is_correct": True,
            "timestamp": datetime.now(timezone.utc)
        }
    ]
    
    for i, interaction_data in enumerate(interactions_data):
        interaction = ManipulativeInteraction(
            id=uuid.UUID(f'55555555-5555-5555-5555-{str(i+1).zfill(12)}'),
            session_id=user_session.id,
            **interaction_data
        )
        session.add(interaction)
    
    print("✓ Created sample manipulative interactions")


def seed_conversation_logs(session, user_session, steps):
    """Seed sample conversation logs"""
    existing_logs = session.query(ConversationLog).filter(
        ConversationLog.session_id == user_session.id
    ).first()
    
    if existing_logs:
        print("✓ Sample conversation logs already exist")
        return
    
    logs_data = [
        {
            "step_id": steps[0].id,
            "speaker": "tutor",
            "message": "Welcome! Today we're going to explore fractions. Can you see the fraction blocks on your screen?",
            "message_type": "instruction",
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "step_id": steps[1].id,
            "speaker": "tutor",
            "message": "Let's start with 1/2. Drag a 1/2 block onto the workspace.",
            "message_type": "instruction",
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "step_id": steps[1].id,
            "speaker": "student",
            "message": "I dragged the 1/2 block!",
            "message_type": "response",
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "step_id": steps[2].id,
            "speaker": "tutor",
            "message": "Now, can you find blocks that look the same size as 1/2? Try dragging a 2/4 block next to it.",
            "message_type": "instruction",
            "timestamp": datetime.now(timezone.utc)
        }
    ]
    
    for i, log_data in enumerate(logs_data):
        log = ConversationLog(
            id=uuid.UUID(f'66666666-6666-6666-6666-{str(i+1).zfill(12)}'),
            session_id=user_session.id,
            **log_data
        )
        session.add(log)
    
    print("✓ Created sample conversation logs")


def main():
    """Run all seed functions"""
    print("Starting seed script...")
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    
    with SessionLocal() as session:
        try:
            # Seed in order
            user = seed_user(session)
            session.commit()
            
            lesson, steps = seed_lesson(session)
            session.commit()
            
            user_session = seed_session(session, user, lesson, steps)
            session.commit()
            
            seed_interactions(session, user_session, steps)
            session.commit()
            
            seed_conversation_logs(session, user_session, steps)
            session.commit()
            
            print("\n✓ All seeds completed successfully!")
            
        except Exception as e:
            session.rollback()
            print(f"\n✗ Error seeding database: {e}")
            raise


if __name__ == "__main__":
    main()
