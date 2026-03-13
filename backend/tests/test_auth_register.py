"""
Tests for POST /auth/register endpoint
Following TDD: These tests must fail first, then we implement to make them pass
"""
import pytest
from fastapi import status


def test_register_returns_token_and_user(client):
    """Test that registration returns a token and user data"""
    response = client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "password123",
            "name": "John Doe"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check response structure
    assert "data" in data
    assert data["error"] is None
    
    # Check user data
    assert "user" in data["data"]
    user = data["data"]["user"]
    assert user["email"] == "student@example.com"
    assert user["name"] == "John Doe"
    assert "id" in user
    assert "created_at" in user
    assert "password" not in user  # Password should never be in response
    
    # Check token
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"
    assert len(data["data"]["access_token"]) > 0


def test_register_creates_user_in_database(client, db_session):
    """Test that registration actually creates a user in the database"""
    from models.user import User
    
    response = client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "password123",
            "name": "John Doe"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    # Check user exists in database
    user = db_session.query(User).filter(User.email == "student@example.com").first()
    assert user is not None
    assert user.name == "John Doe"
    assert user.password_hash is not None
    assert user.password_hash != "password123"  # Should be hashed


def test_register_hashes_password(client, db_session):
    """Test that password is properly hashed in database"""
    from models.user import User
    from app.core.security import verify_password
    
    response = client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "password123",
            "name": "John Doe"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    # Check password is hashed
    user = db_session.query(User).filter(User.email == "student@example.com").first()
    assert verify_password("password123", user.password_hash) is True
    assert verify_password("wrongpassword", user.password_hash) is False


def test_register_prevents_duplicate_emails(client):
    """Test that registration prevents duplicate email addresses"""
    # Register first user
    response1 = client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "password123",
            "name": "John Doe"
        }
    )
    assert response1.status_code == status.HTTP_200_OK
    
    # Try to register same email again
    response2 = client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "password456",
            "name": "Jane Doe"
        }
    )
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert response2.json()["error"] is not None
