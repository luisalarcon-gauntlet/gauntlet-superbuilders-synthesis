"""
Verification script to check database setup
"""
import sys
import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from config import DATABASE_URL
except ImportError:
    from backend.config import DATABASE_URL


def verify_connection():
    """Verify database connection"""
    print("1. Testing database connection...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("   ✓ Database connection successful")
        return engine
    except OperationalError as e:
        print(f"   ✗ Database connection failed: {e}")
        return None


def verify_tables(engine):
    """Verify all tables exist"""
    print("\n2. Verifying tables exist...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = [
        'users',
        'lessons',
        'lesson_steps',
        'user_sessions',
        'manipulative_interactions',
        'conversation_logs'
    ]
    
    missing_tables = []
    for table in expected_tables:
        if table in tables:
            print(f"   ✓ Table '{table}' exists")
        else:
            print(f"   ✗ Table '{table}' missing")
            missing_tables.append(table)
    
    return len(missing_tables) == 0


def verify_columns(engine):
    """Verify table columns match spec"""
    print("\n3. Verifying table columns...")
    inspector = inspect(engine)
    
    # Expected columns for each table
    expected_columns = {
        'users': ['id', 'name', 'created_at', 'updated_at'],
        'lessons': ['id', 'title', 'description', 'topic', 'difficulty_level', 'is_active', 'created_at', 'updated_at'],
        'lesson_steps': ['id', 'lesson_id', 'step_number', 'step_type', 'tutor_message', 'expected_action', 'success_message', 'hint_message', 'created_at', 'updated_at'],
        'user_sessions': ['id', 'user_id', 'lesson_id', 'status', 'current_step_id', 'started_at', 'completed_at', 'created_at', 'updated_at'],
        'manipulative_interactions': ['id', 'session_id', 'step_id', 'interaction_type', 'fraction_value', 'position_x', 'position_y', 'is_correct', 'timestamp', 'created_at', 'updated_at'],
        'conversation_logs': ['id', 'session_id', 'step_id', 'speaker', 'message', 'message_type', 'timestamp', 'created_at', 'updated_at']
    }
    
    all_correct = True
    for table_name, expected_cols in expected_columns.items():
        try:
            columns = [col['name'] for col in inspector.get_columns(table_name)]
            missing = set(expected_cols) - set(columns)
            extra = set(columns) - set(expected_cols)
            
            if missing:
                print(f"   ✗ Table '{table_name}' missing columns: {missing}")
                all_correct = False
            elif extra:
                print(f"   ⚠ Table '{table_name}' has extra columns: {extra}")
            else:
                print(f"   ✓ Table '{table_name}' has correct columns")
        except Exception as e:
            print(f"   ✗ Error checking table '{table_name}': {e}")
            all_correct = False
    
    return all_correct


def verify_foreign_keys(engine):
    """Verify foreign key constraints"""
    print("\n4. Verifying foreign key constraints...")
    inspector = inspect(engine)
    
    expected_fks = {
        'lesson_steps': ['lesson_id -> lessons.id'],
        'user_sessions': ['user_id -> users.id', 'lesson_id -> lessons.id', 'current_step_id -> lesson_steps.id'],
        'manipulative_interactions': ['session_id -> user_sessions.id', 'step_id -> lesson_steps.id'],
        'conversation_logs': ['session_id -> user_sessions.id', 'step_id -> lesson_steps.id']
    }
    
    all_correct = True
    for table_name, expected_fk_descriptions in expected_fks.items():
        try:
            fks = inspector.get_foreign_keys(table_name)
            fk_pairs = [f"{fk['constrained_columns'][0]} -> {fk['referred_table']}.{fk['referred_columns'][0]}" for fk in fks]
            
            for expected_fk in expected_fk_descriptions:
                if expected_fk in fk_pairs:
                    print(f"   ✓ Foreign key '{expected_fk}' exists in '{table_name}'")
                else:
                    print(f"   ✗ Foreign key '{expected_fk}' missing in '{table_name}'")
                    all_correct = False
        except Exception as e:
            print(f"   ✗ Error checking foreign keys for '{table_name}': {e}")
            all_correct = False
    
    return all_correct


def verify_seed_data(engine):
    """Verify seed data exists"""
    print("\n5. Verifying seed data...")
    
    with engine.connect() as conn:
        # Check for test user
        result = conn.execute(text("SELECT COUNT(*) FROM users WHERE name = 'Test Student'"))
        user_count = result.scalar()
        if user_count > 0:
            print("   ✓ Test user exists")
        else:
            print("   ✗ Test user missing")
            return False
        
        # Check for lesson
        result = conn.execute(text("SELECT COUNT(*) FROM lessons WHERE title = 'Fraction Equivalence'"))
        lesson_count = result.scalar()
        if lesson_count > 0:
            print("   ✓ Fraction Equivalence lesson exists")
        else:
            print("   ✗ Fraction Equivalence lesson missing")
            return False
        
        # Check for lesson steps
        result = conn.execute(text("SELECT COUNT(*) FROM lesson_steps"))
        steps_count = result.scalar()
        if steps_count >= 8:
            print(f"   ✓ Found {steps_count} lesson steps")
        else:
            print(f"   ✗ Expected at least 8 lesson steps, found {steps_count}")
            return False
        
        # Check for session
        result = conn.execute(text("SELECT COUNT(*) FROM user_sessions WHERE status = 'in_progress'"))
        session_count = result.scalar()
        if session_count > 0:
            print("   ✓ Sample session exists")
        else:
            print("   ✗ Sample session missing")
            return False
    
    return True


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Database Verification Script")
    print("=" * 60)
    
    engine = verify_connection()
    if not engine:
        print("\n✗ Cannot proceed without database connection")
        sys.exit(1)
    
    tables_ok = verify_tables(engine)
    columns_ok = verify_columns(engine)
    fks_ok = verify_foreign_keys(engine)
    seed_ok = verify_seed_data(engine)
    
    print("\n" + "=" * 60)
    if tables_ok and columns_ok and fks_ok and seed_ok:
        print("✓ All verifications passed!")
        sys.exit(0)
    else:
        print("✗ Some verifications failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
