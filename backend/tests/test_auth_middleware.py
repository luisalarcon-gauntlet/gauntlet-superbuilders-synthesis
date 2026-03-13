"""
Tests for JWT middleware that protects routes
Following TDD: These tests must fail first, then we implement to make them pass
"""
import pytest
from fastapi import status


def test_protected_route_returns_401_without_token(client):
    """Test that a protected route returns 401 without token"""
    # Try to access a protected route without token
    response = client.get("/auth/protected-test")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["error"] is not None


def test_protected_route_works_with_valid_token(client):
    """Test that a protected route works with valid token"""
    # Register and get token
    register_response = client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "password123",
            "name": "John Doe"
        }
    )
    token = register_response.json()["data"]["access_token"]
    
    # Access protected route with token
    response = client.get(
        "/auth/protected-test",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "student@example.com"


def test_protected_route_fails_with_invalid_token(client):
    """Test that a protected route fails with invalid token"""
    response = client.get(
        "/auth/protected-test",
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["error"] is not None


def test_protected_route_fails_with_expired_token(client):
    """Test that a protected route fails with expired token"""
    # This test will need a way to create an expired token
    # For now, we'll test with a malformed token
    response = client.get(
        "/auth/protected-test",
        headers={"Authorization": "Bearer expired_token"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
