# Database Schema & Migrations

## Overview

Agent 2 implemented the complete database schema for the Synthesis Math Tutor application, including SQLAlchemy models, Alembic migrations, and seed data. All models match the specification exactly, with proper relationships, constraints, and automatic migration execution on container startup.

## What Was Built

### 1. Database Models

Created 6 SQLAlchemy models following the `.cursor/rules/db.mdc` conventions:

#### User Model (`backend/models/user.py`)
- **Fields**: `id` (UUID), `name`, `email`, `password_hash`, `created_at`, `updated_at`
- **Purpose**: Stores student user information
- **Key Features**: UUID primary key, timestamps, email field (added by Agent 3 for authentication)

#### Lesson Model (`backend/models/lesson.py`)
- **Fields**: `id` (UUID), `title`, `description`, `topic`, `difficulty_level`, `is_active`, `created_at`, `updated_at`
- **Purpose**: Defines available math lessons
- **Relationships**: One-to-many with `LessonStep` and `UserSession`
- **Key Features**: Tracks lesson metadata, supports multiple lessons in future

#### LessonStep Model (`backend/models/lesson_step.py`)
- **Fields**: `id` (UUID), `lesson_id`, `step_number`, `step_type`, `tutor_message`, `expected_action`, `success_message`, `hint_message`, `created_at`, `updated_at`
- **Purpose**: Sequential steps within lessons
- **Relationships**: Many-to-one with `Lesson` (CASCADE delete)
- **Key Features**: Supports different step types (exploration, assessment, etc.)

#### UserSession Model (`backend/models/user_session.py`)
- **Fields**: `id` (UUID), `user_id`, `lesson_id`, `status`, `current_step_id`, `started_at`, `completed_at`, `created_at`, `updated_at`
- **Purpose**: Tracks individual learning sessions
- **Relationships**: 
  - Many-to-one with `User` (CASCADE delete)
  - Many-to-one with `Lesson` (CASCADE delete)
  - Many-to-one with `LessonStep` (SET NULL on step delete)
- **Key Features**: Progress tracking via `current_step_id`, session state management

#### ManipulativeInteraction Model (`backend/models/manipulative_interaction.py`)
- **Fields**: `id` (UUID), `session_id`, `step_id`, `interaction_type`, `fraction_value`, `position_x`, `position_y`, `is_correct`, `timestamp`, `created_at`, `updated_at`
- **Purpose**: Records student interactions with fraction manipulatives
- **Relationships**: Many-to-one with `UserSession` and `LessonStep` (CASCADE delete)
- **Key Features**: Tracks drag-and-drop actions, block positions, correctness

#### ConversationLog Model (`backend/models/conversation_log.py`)
- **Fields**: `id` (UUID), `session_id`, `step_id`, `speaker`, `message`, `message_type`, `timestamp`, `created_at`, `updated_at`
- **Purpose**: Stores conversational flow between tutor and student
- **Relationships**: Many-to-one with `UserSession` and `LessonStep` (CASCADE delete)
- **Key Features**: Complete conversation history, supports different message types

### 2. Base Model Architecture

**Created**: `BaseModel` with `TimestampMixin` (`backend/models/base.py`)

**Features**:
- UUID primary keys for all tables
- Automatic timestamp management (`created_at`, `updated_at`)
- Reusable `to_dict()` method for serialization
- `get_by_id()` class method for easy lookups
- PostgreSQL's `TIMEZONE('utc', NOW())` for server-side timestamp defaults

**Decision**: Base model pattern over repeating code in each model.

**Rationale**:
- DRY principle - avoid repeating timestamp and UUID logic
- Consistent behavior across all models
- Easier to maintain and update
- Follows SQLAlchemy best practices
- Matches `.cursor/rules/db.mdc` conventions

### 3. Migration Strategy

**Created**: 6 separate Alembic migration files in exact dependency order

**Migration Order**:
1. `001_create_users` - No dependencies
2. `002_create_lessons` - No dependencies
3. `003_create_lesson_steps` - Depends on lessons
4. `004_create_user_sessions` - Depends on users, lessons, lesson_steps
5. `005_create_manipulative_interactions` - Depends on user_sessions, lesson_steps
6. `006_create_conversation_logs` - Depends on user_sessions, lesson_steps

**Decision**: Separate migrations over single migration file.

**Rationale**:
- Respects foreign key dependencies
- Each migration is atomic and reversible
- Follows Alembic best practices (one logical change per migration)
- Easier to debug and rollback if needed
- Clear migration history

**Key Migration Features**:
- All foreign keys properly defined with constraints
- `CASCADE` delete for most relationships (cleanup on parent delete)
- `SET NULL` for `current_step_id` in user_sessions (preserves session if step deleted)
- All timestamps use `TIMEZONE('utc', NOW())` for consistency
- UUID columns use PostgreSQL's UUID type
- Proper indexes on foreign keys and frequently queried columns

### 4. Alembic Configuration

**Files Created**:
- `backend/alembic.ini` - Alembic configuration file
- `backend/alembic/env.py` - Migration environment with model imports
- `backend/alembic/script.py.mako` - Migration template

**Configuration Decisions**:
- Uses `DATABASE_URL` from `backend/config.py` (reads from environment)
- Imports all models so Alembic can autogenerate future migrations
- Configured for PostgreSQL with UUID support
- Proper revision chain management

**Decision**: Automatic model detection over manual migration writing.

**Rationale**:
- Alembic can autogenerate migrations from model changes
- Reduces manual migration writing errors
- Easier to maintain as models evolve
- Still allows manual migration editing when needed

### 5. Automatic Migration on Startup

**Created**: `backend/run_migrations.py` and `backend/start.sh`

**Implementation Flow**:
1. `run_migrations.py` waits for database to be ready (retries with exponential backoff)
2. Runs `alembic upgrade head` to apply all pending migrations
3. `start.sh` orchestrates: migrations → seed → start app

**Decision**: Run migrations on container startup, not in Dockerfile build.

**Rationale**:
- Database may not be available during Docker build
- Ensures migrations run on every container start
- Handles database connection timing gracefully
- Idempotent - safe to run multiple times
- Works in both development and production

**Key Features**:
- Exponential backoff retry logic for database connection
- Clear error messages if database unavailable
- Non-blocking - doesn't prevent app startup if migrations fail (logs error)
- Integrated into container startup flow

### 6. Seed Data

**Created**: `backend/db/seed.py` with minimal happy path testing data

**Seed Data Includes**:
1. **Test User**: "Test Student" (UUID: `11111111-1111-1111-1111-111111111111`)
2. **Fraction Equivalence Lesson**: Complete lesson with 8 steps covering:
   - Welcome and exploration introduction
   - Fraction manipulative exploration (1/2, 2/4 blocks)
   - Guided discovery questions
   - Equivalence comparison activities
   - Final comprehension check
3. **Sample Session**: In-progress session on step 3
4. **Sample Interactions**: 3 manipulative interactions (drag 1/2, drag 2/4, compare)
5. **Sample Conversation Logs**: 4 conversation messages showing tutor-student flow

**Decision**: Minimal seed data over comprehensive test data.

**Rationale**:
- Uses fixed UUIDs for consistency and idempotency
- Idempotent design - checks for existing data before creating
- Covers complete lesson flow for immediate testing
- Minimal but sufficient for happy path validation
- Can be extended later as needed

**Key Design Decisions**:
- All seed functions check for existing data before creating (idempotent)
- Uses `session.flush()` to get IDs before creating related records
- Fixed UUIDs enable predictable testing and data relationships
- Safe to run multiple times without creating duplicates

### 7. Import Strategy

**Decision**: Try/except pattern for imports to support both absolute and relative imports.

**Implementation**: Model files use relative imports (`from models.base import BaseModel`), but seed script uses try/except to support both:
- Running from `backend/` directory (relative imports)
- Running with PYTHONPATH including workspace root (absolute imports)

**Rationale**:
- Works when running from `backend/` directory (relative imports)
- Works when PYTHONPATH includes workspace root (absolute imports)
- Ensures compatibility with both Docker and local development
- Flexible without breaking either environment

## Key Decisions Made

### 1. UUID Primary Keys
**Decision**: All tables use UUID primary keys (not auto-incrementing integers).

**Why**: 
- Matches specification exactly
- Better for distributed systems
- Avoids ID collision issues
- Follows `.cursor/rules/db.mdc` conventions
- More secure (doesn't expose record count)

### 2. Timestamp Mixin
**Decision**: Created `TimestampMixin` for consistent timestamp management.

**Why**:
- DRY principle - avoid repeating timestamp columns
- Consistent UTC timezone handling
- Server-side defaults ensure accuracy
- Easier to maintain

### 3. Foreign Key Cascade Behavior
**Decision**: 
- Most FKs use `CASCADE` delete
- `current_step_id` uses `SET NULL`

**Why**:
- Prevents orphaned records (CASCADE)
- Preserves sessions if steps are deleted (SET NULL allows session to continue)
- Matches business logic (sessions should survive step changes)

### 4. Migration Automation
**Decision**: Run migrations on container startup, not in Dockerfile build.

**Why**:
- Database may not be available during build
- Ensures migrations run on every container start
- Handles database connection timing gracefully
- Works in both development and production

### 5. Seed Data Location
**Decision**: Created seed in both `db/seed.py` (root) and `backend/db/seed.py` (for Docker).

**Why**:
- Root location for easy access
- Backend location matches Docker build context
- Both are identical, just different paths
- Supports both development workflows

## What Was Skipped/Deferred

### 1. Database Indexing Strategy
**Skipped**: Comprehensive indexing beyond foreign keys.

**Why**: Focus on schema first. Indexes can be added based on query patterns as application grows.

### 2. Database Constraints Beyond Foreign Keys
**Skipped**: Check constraints, unique constraints beyond email.

**Why**: Basic constraints sufficient for MVP. Additional constraints can be added as needed.

### 3. Database Views
**Skipped**: Materialized views or database views for complex queries.

**Why**: Not needed for initial implementation. Can be added if query performance requires it.

### 4. Database Triggers
**Skipped**: Database-level triggers for automatic updates.

**Why**: Application-level logic is sufficient and more maintainable. Triggers can be added if needed.

### 5. Database Partitioning
**Skipped**: Table partitioning for large datasets.

**Why**: Not needed for MVP scale. Can be added if data volume requires it.

## Problems Encountered & Resolutions

### 1. Database Connection Timing
**Problem**: Migrations running before database is ready.

**Resolution**: Created `run_migrations.py` with exponential backoff retry logic to wait for database readiness.

### 2. Import Path Issues
**Problem**: Different import paths needed for Docker vs local development.

**Resolution**: Used try/except pattern in seed script to support both absolute and relative imports.

### 3. Foreign Key Dependency Order
**Problem**: Migrations failing due to incorrect dependency order.

**Resolution**: Created migrations in exact dependency order (001-006) ensuring parent tables exist before child tables.

### 4. Timestamp Timezone Consistency
**Problem**: Ensuring all timestamps use UTC consistently.

**Resolution**: Used PostgreSQL's `TIMEZONE('utc', NOW())` function in all timestamp defaults.

### 5. Seed Data Idempotency
**Problem**: Seed script creating duplicate data on multiple runs.

**Resolution**: Added existence checks before creating seed data, making seed script idempotent.

### 6. UUID Type Support
**Problem**: Alembic not recognizing UUID columns correctly.

**Resolution**: Used `sqlalchemy.dialects.postgresql.UUID` type explicitly in models.

## Verification

### Database Verification Script
Created `backend/verify_db.py` to validate:
- Database connection
- All 6 tables exist
- All columns match specification
- Foreign key constraints are present
- Seed data exists

### Migration Validation
- All 6 migrations created in correct dependency order
- Foreign key constraints properly defined
- Migration chain validates (Alembic can walk revisions)
- All syntax verified

### Seed Script Validation
- Seed script syntax verified
- All imports resolve correctly
- Idempotent design tested (can run multiple times safely)

## Files Created/Modified

```
backend/
├── alembic.ini                 # Alembic configuration
├── alembic/
│   ├── env.py                  # Migration environment
│   ├── script.py.mako          # Migration template
│   └── versions/               # Migration files (6 files)
│       ├── 001_create_users.py
│       ├── 002_create_lessons.py
│       ├── 003_create_lesson_steps.py
│       ├── 004_create_user_sessions.py
│       ├── 005_create_manipulative_interactions.py
│       └── 006_create_conversation_logs.py
├── config.py                   # Configuration management (existing)
├── db/
│   └── seed.py                 # Seed script
├── models/
│   ├── __init__.py             # Model exports
│   ├── base.py                 # BaseModel and TimestampMixin
│   ├── user.py                 # User model
│   ├── lesson.py               # Lesson model
│   ├── lesson_step.py          # LessonStep model
│   ├── user_session.py         # UserSession model
│   ├── manipulative_interaction.py  # ManipulativeInteraction model
│   └── conversation_log.py     # ConversationLog model
├── run_migrations.py           # Migration runner
├── start.sh                    # Startup script (updated)
├── verify_db.py                # Database verification script
├── Dockerfile                  # Updated with migration support
└── requirements.txt            # Updated with SQLAlchemy, Alembic, psycopg2-binary
```

## Next Steps

After database schema setup, the next agent (Agent 3) would:
1. Add authentication fields to User model (email, password_hash)
2. Create authentication endpoints
3. Implement JWT token management

The database foundation was ready for authentication and API development.
