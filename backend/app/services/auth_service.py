"""
Authentication service - business logic for auth operations
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.models.auth import UserResponse, AuthResponse
from fastapi import HTTPException, status
from uuid import UUID


def register_user(db: Session, email: str, password: str, name: str) -> AuthResponse:
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = hash_password(password)
    
    # Create user
    user = User(
        email=email,
        password_hash=password_hash,
        name=name
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create access token
    access_token = create_access_token(str(user.id))
    
    # Return response
    return AuthResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        token_type="bearer"
    )


def login_user(db: Session, email: str, password: str) -> AuthResponse:
    """Login a user"""
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(str(user.id))
    
    # Return response
    return AuthResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        token_type="bearer"
    )


def get_user_by_id(db: Session, user_id: UUID) -> User:
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
