"""
Tests for POST /auth/login endpoint
Following TDD: These tests must fail first, then we implement to make them pass
"""
import pytest
from fastapi import status


def test_login_returns_token_and_user(client):
    """Test that login returns a token and user data"""
    # First register a user
    client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "password123",
            "name": "John Doe"
        }
    )
    
    # Now try to login
    response = client.post(
        "/auth/login",
        json={
            "email": "student@example.com",
            "password": "password123"
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
    assert "password" not in user  # Password should never be in response
    
    # Check token
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"
    assert len(data["data"]["access_token"]) > 0


def test_login_fails_with_wrong_password(client):
    """Test that login fails with incorrect password"""
    # First register a user
    client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "password123",
            "name": "John Doe"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/auth/login",
        json={
            "email": "student@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["data"] is None
    assert data["error"] is not None


def test_login_fails_with_nonexistent_email(client):
    """Test that login fails with email that doesn't exist"""
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["data"] is None
    assert data["error"] is not None
