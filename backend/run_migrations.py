"""
Run Alembic migrations automatically
"""
import sys
import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from backend.config import DATABASE_URL
except ImportError:
    from config import DATABASE_URL


def wait_for_db(max_retries=30, retry_delay=2):
    """Wait for database to be ready"""
    engine = create_engine(DATABASE_URL)
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✓ Database is ready")
            return True
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Waiting for database... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print(f"✗ Database not available after {max_retries} attempts")
                raise
    return False


def run_migrations():
    """Run Alembic migrations"""
    from alembic.config import Config
    from alembic import command
    
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    
    print("Running database migrations...")
    try:
        command.upgrade(alembic_cfg, "head")
        print("✓ Migrations completed successfully")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        raise


if __name__ == "__main__":
    print("Starting migration process...")
    wait_for_db()
    run_migrations()
