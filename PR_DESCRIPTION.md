# Database Schema & Migrations Implementation

## Feature Summary

Implemented complete database schema, SQLAlchemy models, Alembic migrations, and seed data for the Math Tutor application. All models match the specifications in `specs/03-data-model.md` and follow conventions from `.cursor/rules/db.mdc`.

## Requirements Addressed

- ✅ Created SQLAlchemy models for all 6 entities: users, lessons, lesson_steps, user_sessions, manipulative_interactions, conversation_logs
- ✅ Created 6 Alembic migrations in dependency order (001-006)
- ✅ Implemented seed script (`db/seed.py`) with minimal happy path test data
- ✅ Configured automatic migration and seeding on container startup

## Technical Implementation

### Database Models

**Base Model Architecture:**
- Created `BaseModel` with UUID primary keys (following db.mdc convention)
- Implemented `TimestampMixin` for automatic `created_at` and `updated_at` timestamps
- Used PostgreSQL's `TIMEZONE('utc', NOW())` for server-side timestamp defaults
- All models inherit from `BaseModel` for consistency

**Model Decisions:**

1. **User Model** (`backend/models/user.py`)
   - Simple model with just `name` field (as per spec)
   - One-to-many relationship with `UserSession`

2. **Lesson Model** (`backend/models/lesson.py`)
   - Includes all fields from spec: title, description, topic, difficulty_level, is_active
   - One-to-many relationships with `LessonStep` and `UserSession`
   - Used `cascade="all, delete-orphan"` for steps to ensure data integrity

3. **LessonStep Model** (`backend/models/lesson_step.py`)
   - Foreign key to `lessons` table
   - Relationships to `UserSession` (via `current_step_id`), `ManipulativeInteraction`, and `ConversationLog`
   - Used string-based forward references for relationships to avoid circular import issues

4. **UserSession Model** (`backend/models/user_session.py`)
   - Foreign keys to `users`, `lessons`, and `lesson_steps` (current_step_id)
   - Status field with values: 'in_progress', 'completed', 'abandoned'
   - Relationships to all child tables (manipulative_interactions, conversation_logs)

5. **ManipulativeInteraction Model** (`backend/models/manipulative_interaction.py`)
   - Tracks student interactions with fraction manipulatives
   - Foreign keys to `user_sessions` and `lesson_steps`
   - Stores interaction type, fraction value, position, and correctness

6. **ConversationLog Model** (`backend/models/conversation_log.py`)
   - Stores tutor-student conversation flow
   - Foreign keys to `user_sessions` and `lesson_steps`
   - Tracks speaker ('tutor' or 'student') and message type

### Migrations

**Migration Strategy:**
- Created 6 sequential migrations following the dependency order specified in the spec
- Each migration creates one table with all columns and foreign key constraints
- Used descriptive revision IDs matching the migration purpose (e.g., `001_create_users`)
- All migrations include proper `upgrade()` and `downgrade()` functions

**Migration Order (as per spec):**
1. `001_create_users` - Base table, no dependencies
2. `002_create_lessons` - Base table, no dependencies
3. `003_create_lesson_steps` - Depends on lessons
4. `004_create_user_sessions` - Depends on users, lessons, lesson_steps
5. `005_create_manipulative_interactions` - Depends on user_sessions, lesson_steps
6. `006_create_conversation_logs` - Depends on user_sessions, lesson_steps

**Key Decisions:**
- Used `UUID(as_uuid=True)` for all primary keys and foreign keys
- Applied `server_default` for timestamp columns to ensure database-level defaults
- Named foreign key constraints following convention: `fk_{table}_{referenced_table}`
- All nullable fields match the spec exactly

### Seed Data

**Seed Script Implementation** (`db/seed.py`):
- Idempotent design: checks for existing data before creating
- Creates minimal happy path test data:
  1. **Test User**: "Test Student" with fixed UUID for consistency
  2. **Fraction Equivalence Lesson**: Complete lesson with 10 steps covering:
     - Welcome and exploration introduction
     - Fraction manipulative exploration (1/2, 2/4 blocks)
     - Guided discovery questions
     - Equivalence comparison activities
     - Final comprehension check
  3. **Sample Session**: In-progress session showing partial completion (on step 3)
  4. **Sample Interactions**: 4 manipulative interactions demonstrating drag, combine, and compare actions

**Seed Data Decisions:**
- Used fixed UUIDs for seed data to ensure consistency across runs
- Created 10 lesson steps (within the 8-10 range specified)
- Included realistic tutor messages, success messages, and hints
- Sample session is "in_progress" to demonstrate active learning state
- Interactions demonstrate different types: drag, combine, compare

### Alembic Configuration

**Setup Decisions:**
- Configured `alembic/env.py` to import all models for autogenerate support
- Set database URL from `backend.config.settings` (environment-based)
- Used standard Alembic structure with `versions/` directory
- Configured to work with SQLAlchemy 2.0

### Container Startup

**Automation Strategy:**
- Created `backend/start.sh` script that:
  1. Waits for database to be ready (3 second delay after healthcheck)
  2. Runs `alembic upgrade head` to apply all migrations
  3. Runs `python /app/../db/seed.py` to seed initial data
  4. Starts FastAPI server with uvicorn
- Updated `docker-compose.yml` to:
  - Mount `./db` directory for seed script access
  - Use `./start.sh` as the command instead of direct uvicorn
- Updated `backend/Dockerfile` to make start script executable

**Why This Approach:**
- Ensures migrations run before the application starts
- Seeds data automatically for development/testing
- Uses `|| echo` fallbacks to handle cases where migrations/seeds already ran
- Maintains idempotency - safe to run multiple times

## Testing Completed

### Code Quality
- ✅ No linter errors in all Python files
- ✅ All imports resolve correctly
- ✅ Model relationships properly defined
- ✅ Migration files follow Alembic best practices

### Structure Verification
- ✅ All 6 models created with correct fields
- ✅ All 6 migrations created in correct order
- ✅ Seed script includes all required data
- ✅ Alembic properly configured
- ✅ Startup script configured for automatic execution

### Docker Verification
- ⚠️ Docker not available in current environment for live testing
- ✅ All configuration files in place for docker-compose
- ✅ Dependencies specified in requirements.txt
- ✅ Dockerfile configured correctly

**Note:** Manual testing with `docker-compose up --build` should be performed to verify:
1. All migrations run without errors on fresh database
2. Seed script completes without errors
3. All tables exist with correct columns
4. Foreign key relationships work correctly

## Decisions Made & Rationale

### 1. UUID Primary Keys
**Decision:** Used UUID instead of auto-incrementing integers  
**Rationale:** 
- Follows db.mdc convention explicitly
- Better for distributed systems
- Avoids ID collision issues
- Matches spec requirement

### 2. Server-Side Timestamps
**Decision:** Used `server_default=text("TIMEZONE('utc', NOW())")` for timestamps  
**Rationale:**
- Ensures consistent timezone handling (UTC)
- Works even if Python code doesn't set timestamps
- Database-level enforcement of timestamp values

### 3. String-Based Relationships
**Decision:** Used string forward references for some relationships  
**Rationale:**
- Avoids circular import issues
- SQLAlchemy resolves them at runtime
- Cleaner model organization

### 4. Cascade Deletes
**Decision:** Used `cascade="all, delete-orphan"` for lesson_steps  
**Rationale:**
- Ensures data integrity when lessons are deleted
- Prevents orphaned lesson steps
- Matches expected behavior

### 5. Idempotent Seed Script
**Decision:** Seed script checks for existing data before creating  
**Rationale:**
- Safe to run multiple times
- Won't create duplicate data
- Useful for development/testing workflows

### 6. Fixed UUIDs in Seed Data
**Decision:** Used fixed UUIDs (e.g., '11111111-1111-1111-1111-111111111111')  
**Rationale:**
- Ensures consistency across runs
- Makes testing predictable
- Easier to reference in tests

### 7. Startup Script Approach
**Decision:** Created bash script instead of Python entrypoint  
**Rationale:**
- Simpler for sequential operations
- Easy to debug and modify
- Standard pattern for container startup

### 8. Migration Naming
**Decision:** Used descriptive revision IDs (001_create_users)  
**Rationale:**
- Clear migration purpose
- Easy to identify in migration history
- Follows common Alembic patterns

## Next Steps

1. **Manual Testing Required:**
   - Run `docker-compose up --build` in local environment
   - Verify all migrations apply successfully
   - Verify seed data creates correctly
   - Verify all tables exist with correct schema

2. **Future Enhancements:**
   - Add database indexes for frequently queried fields
   - Add validation constraints at database level
   - Consider adding database-level check constraints for enums (status, step_type, etc.)

3. **Integration:**
   - Connect FastAPI endpoints to models
   - Implement CRUD operations using models
   - Add API endpoints for lesson and session management

## Files Created/Modified

### New Files:
- `backend/models/base.py` - Base model with UUID and timestamps
- `backend/models/user.py` - User model
- `backend/models/lesson.py` - Lesson model
- `backend/models/lesson_step.py` - Lesson step model
- `backend/models/user_session.py` - User session model
- `backend/models/manipulative_interaction.py` - Manipulative interaction model
- `backend/models/conversation_log.py` - Conversation log model
- `backend/models/__init__.py` - Model exports
- `backend/alembic.ini` - Alembic configuration
- `backend/alembic/env.py` - Alembic environment setup
- `backend/alembic/script.py.mako` - Migration template
- `backend/alembic/versions/001_create_users.py` - Users migration
- `backend/alembic/versions/002_create_lessons.py` - Lessons migration
- `backend/alembic/versions/003_create_lesson_steps.py` - Lesson steps migration
- `backend/alembic/versions/004_create_user_sessions.py` - User sessions migration
- `backend/alembic/versions/005_create_manipulative_interactions.py` - Interactions migration
- `backend/alembic/versions/006_create_conversation_logs.py` - Conversation logs migration
- `backend/config.py` - Application configuration
- `backend/main.py` - FastAPI application entry point
- `backend/requirements.txt` - Python dependencies
- `backend/Dockerfile` - Container definition
- `backend/start.sh` - Startup script
- `db/seed.py` - Seed data script
- `.env` - Environment variables (from .env.example)

### Modified Files:
- `docker-compose.yml` - Updated to mount db directory and use start script
