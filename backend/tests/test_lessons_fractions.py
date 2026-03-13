"""
Tests for lesson endpoints
"""
import pytest
from uuid import UUID


def get_auth_token(client):
    """Helper to get auth token"""
    register_response = client.post("/auth/register", json={
        "email": "student@test.com",
        "password": "password123",
        "name": "Test Student"
    })
    assert register_response.status_code == 200
    return register_response.json()["data"]["access_token"]


def test_get_lessons_fractions_returns_lesson_and_manipulative_state(client, db_session):
    """Test that GET /lessons/fractions returns lesson data and initial manipulative state"""
    token = get_auth_token(client)
    
    # Make authenticated request to get lesson
    response = client.get(
        "/lessons/fractions",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "data" in data
    assert data["error"] is None
    
    # Check lesson data
    lesson = data["data"]["lesson"]
    assert "id" in lesson
    assert lesson["title"] == "Fraction Equivalence"
    assert lesson["description"] is not None
    assert lesson["status"] == "not_started"
    
    # Check manipulative state
    manipulative_state = data["data"]["manipulative_state"]
    assert "available_blocks" in manipulative_state
    assert "workspace" in manipulative_state
    
    # Check available blocks structure
    available_blocks = manipulative_state["available_blocks"]
    assert len(available_blocks) > 0
    for block in available_blocks:
        assert "id" in block
        assert "type" in block
        assert "color" in block
        assert block["position"] is None  # Initially not placed
    
    # Check workspace structure
    workspace = manipulative_state["workspace"]
    assert "width" in workspace
    assert "height" in workspace
    assert "placed_blocks" in workspace
    assert workspace["placed_blocks"] == []  # Initially empty


def test_start_lesson_creates_session_and_returns_tutor_message(client, db_session):
    """Test that POST /lessons/fractions/start creates a session and returns first tutor message"""
    token = get_auth_token(client)
    
    response = client.post(
        "/lessons/fractions/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "data" in data
    assert data["error"] is None
    
    # Check session data
    session = data["data"]["lesson_session"]
    assert "id" in session
    assert session["status"] == "in_progress"
    assert "started_at" in session
    
    # Check tutor message
    tutor_message = data["data"]["tutor_message"]
    assert "id" in tutor_message
    assert "text" in tutor_message
    assert len(tutor_message["text"]) > 0
    assert "type" in tutor_message
    assert "expects_response" in tutor_message


def test_chat_returns_tutor_message(client, db_session):
    """Test that POST /lessons/fractions/chat returns tutor message"""
    token = get_auth_token(client)
    
    # Start a lesson first
    start_response = client.post(
        "/lessons/fractions/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_response.status_code == 200
    session_id = start_response.json()["data"]["lesson_session"]["id"]
    
    # Send chat message
    response = client.post(
        "/lessons/fractions/chat",
        json={
            "session_id": session_id,
            "message": "I placed the 1/2 block in the workspace",
            "action_type": "text_response"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert data["error"] is None
    assert "tutor_message" in data["data"]
    tutor_message = data["data"]["tutor_message"]
    assert "text" in tutor_message
    assert len(tutor_message["text"]) > 0


def test_action_records_manipulative_action(client, db_session):
    """Test that POST /lessons/fractions/action records action and returns tutor message"""
    token = get_auth_token(client)
    
    # Start a lesson first
    start_response = client.post(
        "/lessons/fractions/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_response.status_code == 200
    session_id = start_response.json()["data"]["lesson_session"]["id"]
    
    # Record action
    response = client.post(
        "/lessons/fractions/action",
        json={
            "session_id": session_id,
            "action": {
                "type": "place_block",
                "block_id": "quarter_1",
                "position": {"x": 100, "y": 200}
            }
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert data["error"] is None
    assert "manipulative_state" in data["data"]
    assert "tutor_message" in data["data"]


def test_combine_blocks_combines_fraction_blocks(client, db_session):
    """Test that POST /lessons/fractions/combine-blocks combines blocks"""
    token = get_auth_token(client)
    
    # Start a lesson first
    start_response = client.post(
        "/lessons/fractions/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_response.status_code == 200
    session_id = start_response.json()["data"]["lesson_session"]["id"]
    
    # Combine blocks
    response = client.post(
        "/lessons/fractions/combine-blocks",
        json={
            "session_id": session_id,
            "block_ids": ["quarter_1", "quarter_2"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert data["error"] is None
    assert "manipulative_state" in data["data"]
    assert "tutor_message" in data["data"]
    assert data["data"]["tutor_message"]["type"] == "revelation"


def test_question_returns_assessment_question(client, db_session):
    """Test that POST /lessons/fractions/question returns a question"""
    token = get_auth_token(client)
    
    # Start a lesson first
    start_response = client.post(
        "/lessons/fractions/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_response.status_code == 200
    session_id = start_response.json()["data"]["lesson_session"]["id"]
    
    # Get question
    response = client.post(
        "/lessons/fractions/question",
        json={"session_id": session_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert data["error"] is None
    assert "question" in data["data"]
    question = data["data"]["question"]
    assert "id" in question
    assert "text" in question
    assert "type" in question
    assert "options" in question
    assert "correct_answer" in question


def test_answer_submits_answer_and_returns_feedback(client, db_session):
    """Test that POST /lessons/fractions/answer submits answer and returns feedback"""
    token = get_auth_token(client)
    
    # Start a lesson first
    start_response = client.post(
        "/lessons/fractions/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_response.status_code == 200
    session_id = start_response.json()["data"]["lesson_session"]["id"]
    
    # Submit answer
    response = client.post(
        "/lessons/fractions/answer",
        json={
            "session_id": session_id,
            "question_id": "q1",
            "answer": "2/4"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert data["error"] is None
    assert "is_correct" in data["data"]
    assert "tutor_message" in data["data"]
    assert data["data"]["is_correct"] is True


def test_progress_returns_lesson_progress(client, db_session):
    """Test that GET /lessons/fractions/progress returns progress"""
    token = get_auth_token(client)
    
    # Start a lesson first
    start_response = client.post(
        "/lessons/fractions/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_response.status_code == 200
    
    # Get progress
    response = client.get(
        "/lessons/fractions/progress",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert data["error"] is None
    assert "session" in data["data"]
    session = data["data"]["session"]
    assert "status" in session
    assert "progress_percentage" in session
    assert "achievements" in data["data"]


def test_complete_marks_lesson_as_completed(client, db_session):
    """Test that POST /lessons/fractions/complete marks lesson as completed"""
    token = get_auth_token(client)
    
    # Start a lesson first
    start_response = client.post(
        "/lessons/fractions/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_response.status_code == 200
    session_id = start_response.json()["data"]["lesson_session"]["id"]
    
    # Complete lesson
    response = client.post(
        "/lessons/fractions/complete",
        json={"session_id": session_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert data["error"] is None
    assert "completion" in data["data"]
    assert "tutor_message" in data["data"]
    completion = data["data"]["completion"]
    assert completion["lesson_completed"] is True
    assert "final_score" in completion
