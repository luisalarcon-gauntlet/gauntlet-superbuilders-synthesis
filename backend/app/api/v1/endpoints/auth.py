"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import register_user, login_user
from app.models.auth import RegisterRequest, LoginRequest, StandardResponse, AuthResponse, UserResponse
from app.api.deps import get_current_user
from models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=StandardResponse)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new student user"""
    try:
        auth_response = register_user(
            db=db,
            email=request.email,
            password=request.password,
            name=request.name
        )
        return StandardResponse(data=auth_response, error=None)
    except HTTPException as e:
        # Return StandardResponse with error and appropriate status code
        status_code = e.status_code
        return Response(
            content=StandardResponse(data=None, error=e.detail).model_dump_json(),
            status_code=status_code,
            media_type="application/json"
        )
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.post("/login", response_model=StandardResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login student user"""
    try:
        auth_response = login_user(
            db=db,
            email=request.email,
            password=request.password
        )
        return StandardResponse(data=auth_response, error=None)
    except HTTPException as e:
        # Return StandardResponse with error and appropriate status code
        status_code = e.status_code
        return Response(
            content=StandardResponse(data=None, error=e.detail).model_dump_json(),
            status_code=status_code,
            media_type="application/json"
        )
    except Exception as e:
        return Response(
            content=StandardResponse(data=None, error=str(e)).model_dump_json(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
        )


@router.get("/protected-test")
async def protected_test(
    current_user: User = Depends(get_current_user)
):
    """Test endpoint for protected routes"""
    return {
        "user": UserResponse.model_validate(current_user).model_dump(),
        "message": "This is a protected route"
    }
