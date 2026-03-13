# Authentication Layer

## Overview

Agent 3 implemented the complete authentication layer for the Synthesis Math Tutor API with JWT-based authentication, password hashing with bcrypt, and protected route middleware. The implementation follows TDD principles with tests written first, then implementation.

## What Was Built

### 1. User Model Extensions

**Modified**: `backend/models/user.py`

**Added Fields**:
- `email` (String(255), unique, indexed, not null)
- `password_hash` (String(255), not null)

**Migration**: Created `007_add_auth_fields_to_users.py` to add these fields to existing users table.

**Decision**: Add fields to existing User model over creating separate Auth model.

**Rationale**:
- Simpler data model - user and auth data together
- Easier queries (no joins needed)
- Matches common authentication patterns
- One-to-one relationship doesn't need separate table

### 2. Password Security

**Created**: `backend/app/core/security.py`

**Implementation**:
- **bcrypt hashing** with 12 salt rounds
- Password verification using constant-time comparison
- Passwords never returned in API responses
- Secure password validation

**Key Functions**:
- `hash_password(password: str) -> str`: Hashes password with bcrypt
- `verify_password(plain_password: str, hashed_password: str) -> bool`: Verifies password

**Decision**: bcrypt with 12 rounds over simpler hashing algorithms.

**Rationale**:
- Industry standard for password hashing
- 12 rounds provides good security/performance balance
- Resistant to rainbow table attacks
- Constant-time verification prevents timing attacks

### 3. JWT Token Management

**Implementation**: `backend/app/core/security.py`

**Features**:
- Token creation with user ID as subject (`sub`)
- Token verification and decoding
- HS256 algorithm with secret key from environment
- Configurable expiration (default: 15 minutes)

**Key Functions**:
- `create_access_token(data: dict, expires_delta: timedelta) -> str`: Creates JWT token
- `decode_token(token: str) -> dict`: Decodes and verifies token

**Configuration**:
- `JWT_SECRET`: From environment variable (required in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Configurable (default: 15)

**Decision**: JWT tokens over session-based authentication.

**Rationale**:
- Stateless - no server-side session storage needed
- Scalable - works across multiple servers
- Matches project requirements (JWT tokens only)
- Industry standard for API authentication

**Decision**: 15-minute expiration over longer sessions.

**Rationale**:
- Limits exposure window if token is compromised
- Forces periodic re-authentication
- Can be extended with refresh tokens later
- Good balance between security and user experience

### 4. Authentication Endpoints

**Created**: `backend/app/api/v1/endpoints/auth.py`

#### POST /auth/register
- **Purpose**: Register new student users
- **Request**: `{email, password, name}`
- **Response**: `{data: {user, access_token, token_type}, error: null}`
- **Status**: 200 on success, 400 on validation error, 500 on server error

**Features**:
- Email validation (format and uniqueness)
- Password hashing before storage
- Automatic token generation on registration
- User creation in database

#### POST /auth/login
- **Purpose**: Login existing users
- **Request**: `{email, password}`
- **Response**: `{data: {user, access_token, token_type}, error: null}`
- **Status**: 200 on success, 401 on invalid credentials, 500 on server error

**Features**:
- Email/password verification
- Token generation on successful login
- Generic error messages (prevents user enumeration)

**Decision**: Generic error messages over specific error details.

**Rationale**:
- Prevents user enumeration attacks
- Doesn't reveal which emails exist in system
- Better security practice
- Still provides enough information for legitimate users

### 5. Protected Route Middleware

**Created**: `backend/app/api/deps.py`

**Implementation**:
- `get_current_user` dependency function
- Extracts token from `Authorization: Bearer <token>` header
- Verifies token validity and expiration
- Returns current user or raises 401 error

**Usage Pattern**:
```python
@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"user": current_user}
```

**Decision**: FastAPI dependency injection over decorator pattern.

**Rationale**:
- Native FastAPI pattern
- Type-safe with Pydantic
- Easy to test and mock
- Flexible - can be combined with other dependencies

### 6. Service Layer

**Created**: `backend/app/services/auth_service.py`

**Purpose**: Separates business logic from HTTP handling

**Functions**:
- `register_user(email, password, name, db) -> User`: Creates new user
- `authenticate_user(email, password, db) -> User | None`: Validates credentials
- `get_user_by_email(email, db) -> User | None`: Finds user by email

**Decision**: Service layer pattern over putting logic in endpoints.

**Rationale**:
- Separation of concerns
- Business logic testable independently
- Easier to maintain and extend
- Reusable across different interfaces (API, CLI, etc.)

### 7. Pydantic Models

**Created**: `backend/app/models/auth.py`

**Request Models**:
- `RegisterRequest`: Email, password, name validation
- `LoginRequest`: Email, password validation

**Response Models**:
- `AuthResponse`: User data, access token, token type
- Uses `StandardResponse` wrapper for consistent format

**Decision**: Pydantic models over manual validation.

**Rationale**:
- Automatic validation
- Type safety
- Clear error messages
- Integrates with FastAPI automatically

### 8. Database Dependencies

**Created**: `backend/app/core/database.py`

**Implementation**:
- `get_db()` dependency function
- Creates database session
- Yields session to route handler
- Closes session after request

**Decision**: Dependency injection for database sessions.

**Rationale**:
- Ensures proper session lifecycle
- Automatic cleanup
- Easy to test with test database
- Follows FastAPI best practices

### 9. Test Suite

**Created**: Comprehensive test suite following TDD principles

**Test Files**:
- `backend/tests/test_auth_register.py`: Registration endpoint tests
- `backend/tests/test_auth_login.py`: Login endpoint tests
- `backend/tests/test_auth_middleware.py`: JWT middleware tests

**Test Coverage**:
- ✅ Registration creates user and returns token
- ✅ Registration hashes passwords correctly
- ✅ Registration prevents duplicate emails
- ✅ Login returns token with correct credentials
- ✅ Login fails with wrong password
- ✅ Login fails with nonexistent email
- ✅ Protected routes require valid token
- ✅ Protected routes reject invalid tokens
- ✅ Protected routes reject expired tokens

**Decision**: TDD approach - tests written first.

**Rationale**:
- Ensures requirements are met
- Tests serve as documentation
- Catches bugs early
- Matches project requirements (TDD cycle)

## Key Decisions Made

### 1. Password Hashing Algorithm
**Decision**: bcrypt with 12 salt rounds.

**Why**: Industry standard, secure, resistant to attacks, good performance/security balance.

### 2. JWT Token Expiration
**Decision**: 15-minute expiration.

**Why**: Limits exposure window, forces periodic re-auth, can extend with refresh tokens later.

### 3. Response Format
**Decision**: Standardized `{data: {...}, error: null}` format.

**Why**: Consistent API responses, easier frontend handling, clear error structure.

### 4. Service Layer Pattern
**Decision**: Separate service layer for business logic.

**Why**: Separation of concerns, testable logic, reusable, maintainable.

### 5. Generic Error Messages
**Decision**: Generic error messages for auth failures.

**Why**: Prevents user enumeration attacks, better security, still usable for legitimate users.

### 6. Email as Username
**Decision**: Email used for authentication (not separate username).

**Why**: Simpler UX, email is unique identifier, common pattern, easier to remember.

## What Was Skipped/Deferred

### 1. Refresh Tokens
**Skipped**: Refresh token mechanism for longer sessions.

**Why**: 15-minute tokens sufficient for MVP. Refresh tokens can be added later for better UX.

### 2. Password Reset
**Skipped**: Password reset functionality.

**Why**: Not required for MVP. Can be added when needed.

### 3. Email Verification
**Skipped**: Email verification for new registrations.

**Why**: Not required for MVP. Can be added for production.

### 4. Rate Limiting
**Skipped**: Rate limiting on auth endpoints.

**Why**: Can be added at infrastructure level. Not critical for MVP.

### 5. Multi-factor Authentication
**Skipped**: 2FA or MFA support.

**Why**: Not required for MVP. Can be added for enhanced security later.

### 6. OAuth/SSO
**Skipped**: OAuth or SSO integration.

**Why**: Not in requirements. JWT-only authentication specified.

## Problems Encountered & Resolutions

### 1. Password Hash Storage
**Problem**: Initial attempt to store passwords in plain text.

**Resolution**: Implemented bcrypt hashing before storage, never storing plain passwords.

### 2. Token Expiration Handling
**Problem**: Expired tokens not properly rejected.

**Resolution**: Added expiration check in token verification, returning 401 for expired tokens.

### 3. Database Session Management
**Problem**: Database sessions not properly closed, causing connection leaks.

**Resolution**: Used FastAPI dependency injection with proper session lifecycle management.

### 4. Email Uniqueness Validation
**Problem**: Race condition allowing duplicate emails.

**Resolution**: Added unique constraint at database level and application-level check.

### 5. Error Message Consistency
**Problem**: Inconsistent error formats across endpoints.

**Resolution**: Standardized on `{data: null, error: "message"}` format for all errors.

### 6. Test Database Setup
**Problem**: Tests interfering with each other due to shared database state.

**Resolution**: Used database transactions with rollback in test fixtures to isolate tests.

## Verification

### Test Execution
All tests written and verified:
- Registration tests pass
- Login tests pass
- Middleware tests pass
- Password hashing verified
- Token generation and validation verified

### Manual Testing
Verified endpoints work correctly:
- Registration creates user and returns token
- Login validates credentials and returns token
- Protected routes require valid token
- Invalid tokens are rejected

### Security Verification
- Passwords are hashed (never stored in plain text)
- Tokens expire after 15 minutes
- Generic error messages prevent enumeration
- Constant-time password comparison

## Files Created/Modified

```
backend/
├── app/
│   ├── core/
│   │   ├── security.py          # JWT and bcrypt utilities
│   │   └── database.py         # Database session management
│   ├── api/
│   │   ├── deps.py             # Dependency injection for auth
│   │   └── v1/
│   │       └── endpoints/
│   │           └── auth.py     # Auth endpoints
│   ├── services/
│   │   └── auth_service.py     # Auth business logic
│   ├── models/
│   │   └── auth.py             # Pydantic models for auth
│   └── main.py                 # Registered auth router
├── models/
│   └── user.py                 # Added email and password_hash fields
├── alembic/versions/
│   └── 007_add_auth_fields_to_users.py  # Migration for auth fields
├── tests/
│   ├── test_auth_register.py    # Registration tests
│   ├── test_auth_login.py      # Login tests
│   └── test_auth_middleware.py # Middleware tests
└── requirements.txt            # Added bcrypt, PyJWT, email-validator, pytest
```

## Next Steps

After authentication setup, the next agent (Agent 4) would:
1. Implement lesson management endpoints
2. Add session tracking
3. Integrate authentication with lesson endpoints

The authentication foundation was ready for protected API endpoints.
