# Data Model Specification - Synthesis Math Tutor Clone

## Overview

This data model supports a conversational AI math tutor focused on teaching fraction equivalence through interactive digital manipulatives. The design prioritizes simplicity and captures essential user interactions, lesson progress, and conversational flow.

## Entities

### users
Stores basic user information for students using the math tutor.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | UUID | No | Primary key |
| name | VARCHAR(255) | No | Student's display name |
| created_at | TIMESTAMP | No | Account creation timestamp |
| updated_at | TIMESTAMP | No | Last update timestamp |

### lessons
Defines the available math lessons in the system.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | UUID | No | Primary key |
| title | VARCHAR(255) | No | Lesson title (e.g., "Fraction Equivalence") |
| description | TEXT | Yes | Lesson description |
| topic | VARCHAR(100) | No | Math topic (e.g., "fractions") |
| difficulty_level | INTEGER | No | Difficulty level 1-10 |
| is_active | BOOLEAN | No | Whether lesson is available |
| created_at | TIMESTAMP | No | Lesson creation timestamp |
| updated_at | TIMESTAMP | No | Last update timestamp |

### lesson_steps
Defines the sequential steps within each lesson.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | UUID | No | Primary key |
| lesson_id | UUID | No | Foreign key to lessons table |
| step_number | INTEGER | No | Order of step in lesson |
| step_type | VARCHAR(50) | No | Type: 'exploration', 'instruction', 'question', 'check' |
| tutor_message | TEXT | No | What the tutor says at this step |
| expected_action | VARCHAR(100) | Yes | Expected student action |
| success_message | TEXT | Yes | Message on correct response |
| hint_message | TEXT | Yes | Hint for incorrect responses |
| created_at | TIMESTAMP | No | Step creation timestamp |
| updated_at | TIMESTAMP | No | Last update timestamp |

**Relationships:**
- lesson_id → lessons.id (Many-to-One)

### user_sessions
Tracks individual learning sessions for progress and analytics.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | UUID | No | Primary key |
| user_id | UUID | No | Foreign key to users table |
| lesson_id | UUID | No | Foreign key to lessons table |
| status | VARCHAR(50) | No | 'in_progress', 'completed', 'abandoned' |
| current_step_id | UUID | Yes | Current lesson step |
| started_at | TIMESTAMP | No | Session start time |
| completed_at | TIMESTAMP | Yes | Session completion time |
| created_at | TIMESTAMP | No | Session creation timestamp |
| updated_at | TIMESTAMP | No | Last update timestamp |

**Relationships:**
- user_id → users.id (Many-to-One)
- lesson_id → lessons.id (Many-to-One)
- current_step_id → lesson_steps.id (Many-to-One)

### manipulative_interactions
Records student interactions with digital fraction manipulatives.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | UUID | No | Primary key |
| session_id | UUID | No | Foreign key to user_sessions table |
| step_id | UUID | No | Foreign key to lesson_steps table |
| interaction_type | VARCHAR(50) | No | 'drag', 'combine', 'split', 'compare' |
| fraction_value | VARCHAR(20) | No | Fraction represented (e.g., "1/2", "2/4") |
| position_x | INTEGER | Yes | X coordinate of manipulative |
| position_y | INTEGER | Yes | Y coordinate of manipulative |
| is_correct | BOOLEAN | Yes | Whether interaction was correct |
| timestamp | TIMESTAMP | No | When interaction occurred |
| created_at | TIMESTAMP | No | Record creation timestamp |
| updated_at | TIMESTAMP | No | Last update timestamp |

**Relationships:**
- session_id → user_sessions.id (Many-to-One)
- step_id → lesson_steps.id (Many-to-One)

### conversation_logs
Stores the conversational flow between tutor and student.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | UUID | No | Primary key |
| session_id | UUID | No | Foreign key to user_sessions table |
| step_id | UUID | No | Foreign key to lesson_steps table |
| speaker | VARCHAR(20) | No | 'tutor' or 'student' |
| message | TEXT | No | Message content |
| message_type | VARCHAR(50) | No | 'instruction', 'question', 'response', 'encouragement' |
| timestamp | TIMESTAMP | No | Message timestamp |
| created_at | TIMESTAMP | No | Record creation timestamp |
| updated_at | TIMESTAMP | No | Last update timestamp |

**Relationships:**
- session_id → user_sessions.id (Many-to-One)
- step_id → lesson_steps.id (Many-to-One)

## Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    users    │    │    lessons      │    │  lesson_steps   │
├─────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)     │    │ id (PK)         │    │ id (PK)         │
│ name        │    │ title           │    │ lesson_id (FK)  │
│ created_at  │    │ description     │    │ step_number     │
│ updated_at  │    │ topic           │    │ step_type       │
└─────────────┘    │ difficulty_level│    │ tutor_message   │
        │          │ is_active       │    │ expected_action │
        │          │ created_at      │    │ success_message │
        │          │ updated_at      │    │ hint_message    │
        │          └─────────────────┘    │ created_at      │
        │                   │             │ updated_at      │
        │                   │             └─────────────────┘
        │                   │                      │
        └───────────┐       │              ┌───────┘
                    │       │              │
            ┌───────▼───────▼──────┐      │
            │   user_sessions      │      │
            ├──────────────────────┤      │
            │ id (PK)              │      │
            │ user_id (FK)         │      │
            │ lesson_id (FK)       │      │
            │ status               │      │
            │ current_step_id (FK) │◄─────┘
            │ started_at           │
            │ completed_at         │
            │ created_at           │
            │ updated_at           │
            └──────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
┌────────▼──────┐ ┌───▼──────────┐  │
│manipulative_  │ │conversation_ │  │
│interactions   │ │logs          │  │
├───────────────┤ ├──────────────┤  │
│ id (PK)       │ │ id (PK)      │  │
│ session_id(FK)│ │session_id(FK)│  │
│ step_id (FK)  │ │ step_id (FK) │◄─┘
│ interaction_  │ │ speaker      │
│ type          │ │ message      │
│ fraction_value│ │ message_type │
│ position_x    │ │ timestamp    │
│ position_y    │ │ created_at   │
│ is_correct    │ │ updated_at   │
│ timestamp     │ └──────────────┘
│ created_at    │
│ updated_at    │
└───────────────┘
```

## Migration Order

Execute migrations in this order to respect foreign key dependencies:

1. `001_create_users.sql`
2. `002_create_lessons.sql`  
3. `003_create_lesson_steps.sql`
4. `004_create_user_sessions.sql`
5. `005_create_manipulative_interactions.sql`
6. `006_create_conversation_logs.sql`

## Seed Data Description

**Minimal seed data for happy path testing:**

1. **Test User**: Create a single user named "Test Student" for development testing
2. **Fraction Equivalence Lesson**: One complete lesson with 8-10 steps covering:
   - Welcome and exploration introduction
   - Fraction manipulative exploration (1/2, 2/4 blocks)
   - Guided discovery questions
   - Equivalence comparison activities  
   - Final comprehension check
3. **Lesson Steps**: Scripted tutor dialogue for each step with appropriate success/hint messages
4. **Sample Session**: One in-progress session showing partial completion
5. **Sample Interactions**: Basic manipulative interactions demonstrating drag, combine, and compare actions with 1/2 and 2/4 fractions

This seed data enables immediate testing of the complete lesson flow, conversational interface, and manipulative interactions without requiring complex setup.