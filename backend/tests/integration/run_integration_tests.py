#!/usr/bin/env python3
"""
Script to run integration tests

This script:
1. Checks if the database is accessible
2. Checks if the API server is running
3. Runs the integration tests

Prerequisites:
1. Database running: docker-compose up -d db
2. Migrations applied: python backend/run_migrations.py
3. Server running: uvicorn app.main:app --reload (in backend directory)
"""
import sys
import subprocess
import time
import httpx
from pathlib import Path

BASE_URL = "http://localhost:8000"
DB_CHECK_TIMEOUT = 10
SERVER_CHECK_TIMEOUT = 10


def check_database():
    """Check if database is accessible"""
    try:
        from config import DATABASE_URL
        from sqlalchemy import create_engine, text
        
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Database is accessible")
        return True
    except Exception as e:
        print(f"✗ Database is not accessible: {e}")
        print("  Please start the database: docker-compose up -d db")
        return False


def check_server():
    """Check if API server is running"""
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        if response.status_code == 200:
            print("✓ API server is running")
            return True
        else:
            print(f"✗ API server returned status {response.status_code}")
            return False
    except httpx.ConnectError:
        print("✗ API server is not running")
        print("  Please start the server: cd backend && uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"✗ Error checking server: {e}")
        return False


def run_tests():
    """Run the integration tests"""
    backend_dir = Path(__file__).parent.parent.parent
    test_dir = Path(__file__).parent
    
    print(f"\nRunning integration tests from {test_dir}...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_dir),
        "-v",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd, cwd=backend_dir)
    return result.returncode == 0


def main():
    """Main entry point"""
    print("Integration Test Runner")
    print("=" * 50)
    
    # Check prerequisites
    print("\nChecking prerequisites...")
    db_ok = check_database()
    server_ok = check_server()
    
    if not db_ok or not server_ok:
        print("\n✗ Prerequisites not met. Please fix the issues above and try again.")
        return 1
    
    # Run tests
    print("\n" + "=" * 50)
    success = run_tests()
    
    if success:
        print("\n✓ All integration tests passed!")
        return 0
    else:
        print("\n✗ Some integration tests failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
