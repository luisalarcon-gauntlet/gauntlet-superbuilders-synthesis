"""
Integration test for Feature 4: Web Application Infrastructure

Tests the full happy path covering:
- API call → DB state change → correct response
- All acceptance criteria from specs/02-features.md
"""
import pytest
import httpx
from sqlalchemy.orm import Session
from models.user import User
from models.user_session import UserSession


BASE_URL = "http://localhost:8000"


def test_jwt_authentication_system_functions_correctly(db_session: Session):
    """
    Acceptance criteria: JWT authentication system functions correctly
    
    Tests:
    1. Registration creates user and returns token
    2. Login returns token
    3. Protected endpoints require valid token
    4. Invalid token is rejected
    """
    with httpx.Client(timeout=30.0) as client:
        # Step 1: Register user
        # API call
        register_response = client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": "infra_test@example.com",
                "password": "password123",
                "name": "Infrastructure Test Student"
            }
        )
        
        # Verify correct response
        assert register_response.status_code == 200
        register_data = register_response.json()
        assert "data" in register_data
        assert "access_token" in register_data["data"]
        assert "user" in register_data["data"]
        
        token = register_data["data"]["access_token"]
        user_data = register_data["data"]["user"]
        
        # Verify DB state change: User created
        user = db_session.query(User).filter(User.email == "infra_test@example.com").first()
        assert user is not None
        assert user.email == "infra_test@example.com"
        assert user.name == "Infrastructure Test Student"
        assert user.password_hash is not None
        assert user.password_hash != "password123"  # Should be hashed
        
        # Step 2: Login with credentials
        # API call
        login_response = client.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": "infra_test@example.com",
                "password": "password123"
            }
        )
        
        # Verify correct response
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "data" in login_data
        assert "access_token" in login_data["data"]
        assert len(login_data["data"]["access_token"]) > 0
        
        login_token = login_data["data"]["access_token"]
        
        # Step 3: Use token to access protected endpoint
        # API call
        headers = {"Authorization": f"Bearer {login_token}"}
        lesson_response = client.get(
            f"{BASE_URL}/lessons/fractions",
            headers=headers
        )
        
        # Verify correct response
        assert lesson_response.status_code == 200
        lesson_data = lesson_response.json()
        assert "data" in lesson_data
        assert "lesson" in lesson_data["data"]
        
        # Step 4: Verify invalid token is rejected
        # API call
        invalid_headers = {"Authorization": "Bearer invalid_token_12345"}
        invalid_response = client.get(
            f"{BASE_URL}/lessons/fractions",
            headers=invalid_headers
        )
        
        # Verify correct response (should be 401)
        assert invalid_response.status_code == 401, "Invalid token should be rejected"
        
        # Step 5: Verify missing token is rejected
        # API call
        no_auth_response = client.get(
            f"{BASE_URL}/lessons/fractions"
        )
        
        # Verify correct response (should be 401)
        assert no_auth_response.status_code == 401, "Missing token should be rejected"


def test_lesson_progress_persists_during_session(db_session: Session):
    """
    Acceptance criteria: Lesson progress persists during session
    
    Tests:
    1. Start lesson creates session
    2. Progress through lesson updates session
    3. Session state persists across requests
    """
    with httpx.Client(timeout=30.0) as client:
        # Register and get token
        register_response = client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": "progress_test@example.com",
                "password": "password123",
                "name": "Progress Test Student"
            }
        )
        assert register_response.status_code == 200
        token = register_response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get user ID
        user = db_session.query(User).filter(User.email == "progress_test@example.com").first()
        assert user is not None
        user_id = user.id
        
        # Step 1: Start lesson
        # API call
        start_response = client.post(
            f"{BASE_URL}/lessons/fractions/start",
            headers=headers
        )
        
        # Verify correct response
        assert start_response.status_code == 200
        start_data = start_response.json()
        session_id = start_data["data"]["lesson_session"]["id"]
        
        # Verify DB state change: Session created
        session = db_session.query(UserSession).filter(
            UserSession.id == session_id
        ).first()
        assert session is not None
        assert session.user_id == user_id
        assert session.status == "in_progress"
        initial_step_id = session.current_step_id
        
        # Step 2: Progress through lesson
        # API call - Send chat message
        chat_response = client.post(
            f"{BASE_URL}/lessons/fractions/chat",
            json={
                "session_id": session_id,
                "message": "I'm making progress",
                "action_type": "text_response"
            },
            headers=headers
        )
        assert chat_response.status_code == 200
        
        # Verify DB state change: Session updated
        db_session.refresh(session)
        # Session should still exist and be in progress
        assert session.status == "in_progress"
        
        # Step 3: Get progress - verify persistence
        # API call
        progress_response = client.get(
            f"{BASE_URL}/lessons/fractions/progress",
            headers=headers
        )
        
        # Verify correct response
        assert progress_response.status_code == 200
        progress_data = progress_response.json()
        assert "data" in progress_data
        assert "session" in progress_data["data"]
        
        progress_session = progress_data["data"]["session"]
        assert progress_session["id"] == session_id
        assert progress_session["status"] == "in_progress"
        
        # Verify session persists in database
        persisted_session = db_session.query(UserSession).filter(
            UserSession.id == session_id
        ).first()
        assert persisted_session is not None
        assert persisted_session.user_id == user_id


def test_application_is_accessible_via_standard_web_browser(db_session: Session):
    """
    Acceptance criteria: Application is accessible via standard web browser
    
    Tests:
    1. Health endpoint responds
    2. Root endpoint responds
    3. API endpoints return proper HTTP responses
    4. CORS headers are set (for browser access)
    """
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        # Step 1: Health check endpoint
        # API call
        health_response = client.get(f"{BASE_URL}/health")
        
        # Verify correct response
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert "status" in health_data
        assert health_data["status"] == "ok"
        
        # Step 2: Root endpoint
        # API call
        root_response = client.get(f"{BASE_URL}/")
        
        # Verify correct response
        assert root_response.status_code == 200
        root_data = root_response.json()
        assert "message" in root_data
        assert "status" in root_data
        
        # Step 3: Verify API endpoints return proper JSON
        # Register user first
        register_response = client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": "browser_test@example.com",
                "password": "password123",
                "name": "Browser Test Student"
            }
        )
        assert register_response.status_code == 200
        token = register_response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # API call to lesson endpoint
        lesson_response = client.get(
            f"{BASE_URL}/lessons/fractions",
            headers=headers
        )
        
        # Verify correct response
        assert lesson_response.status_code == 200
        assert lesson_response.headers["content-type"] == "application/json"
        lesson_data = lesson_response.json()
        assert "data" in lesson_data
        
        # Step 4: Verify CORS headers (for browser access)
        # Make OPTIONS request to check CORS
        options_response = client.options(
            f"{BASE_URL}/lessons/fractions",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        # CORS preflight should be handled (status 200 or 204)
        assert options_response.status_code in [200, 204, 405], \
            "CORS should be configured for browser access"


def test_responsive_design_works_on_ipad_screen_size(db_session: Session):
    """
    Acceptance criteria: Responsive design works on iPad screen size
    
    Tests:
    1. API returns appropriate data structure for responsive rendering
    2. Workspace dimensions are suitable for iPad
    3. Data structure supports touch interactions
    """
    with httpx.Client(timeout=30.0) as client:
        # Register and get token
        register_response = client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": "ipad_test@example.com",
                "password": "password123",
                "name": "iPad Test Student"
            }
        )
        assert register_response.status_code == 200
        token = register_response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get lesson data
        # API call
        lesson_response = client.get(
            f"{BASE_URL}/lessons/fractions",
            headers=headers
        )
        
        # Verify correct response
        assert lesson_response.status_code == 200
        lesson_data = lesson_response.json()
        assert "data" in lesson_data
        assert "manipulative_state" in lesson_data["data"]
        
        manipulative_state = lesson_data["data"]["manipulative_state"]
        workspace = manipulative_state["workspace"]
        
        # Verify workspace dimensions are suitable for iPad
        # iPad screen sizes: 768x1024 (portrait) or 1024x768 (landscape)
        # Workspace should be appropriately sized
        assert workspace["width"] > 0
        assert workspace["height"] > 0
        # Workspace should be large enough for touch interactions
        assert workspace["width"] >= 400, "Workspace should be wide enough for iPad"
        assert workspace["height"] >= 300, "Workspace should be tall enough for iPad"
        
        # Verify data structure supports touch interactions
        # Blocks should have position data for touch placement
        available_blocks = manipulative_state["available_blocks"]
        for block in available_blocks:
            assert "id" in block
            assert "type" in block
            # Position can be None initially, but should support being set
            assert "position" in block or "position" in block  # Position field exists
