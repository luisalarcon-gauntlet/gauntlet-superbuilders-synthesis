# Agent Execution Plan: Synthesis Math Tutor Clone

## Agent 1: Environment & Infrastructure

### What it builds
Sets up Docker-based development environment for a conversational math tutor teaching fraction equivalence. Creates monorepo structure with Next.js frontend for touch-optimized interactions and FastAPI backend for lesson state management.

### Step-by-step instructions
1. Create monorepo structure:
   ```
   synthesis-tutor/
   ├── frontend/          # Next.js app with fraction manipulative UI
   ├── backend/           # FastAPI for lesson progress tracking
   ├── docker-compose.yml # Services: frontend, backend, postgres
   └── README.md
   ```

2. Configure `docker-compose.yml` with services:
   - `frontend`: Next.js on port 3000 (iPad-optimized)
   - `backend`: FastAPI on port 8000 (lesson state API)
   - `postgres`: Database on port 5432 (progress tracking)

3. Create Dockerfiles:
   - Frontend: Node.js with touch-responsive build
   - Backend: Python FastAPI with lesson scripting logic

4. Set up environment variables:
   - `DATABASE_URL` for Postgres connection
   - `JWT_SECRET` for session management
   - `NODE_ENV=development`

### Verification checklist
- [ ] `docker-compose up` starts all three services without errors
- [ ] Frontend accessible at localhost:3000 on desktop browser
- [ ] Backend API docs accessible at localhost:8000/docs
- [ ] Postgres container accepts connections
- [ ] Hot reload works for both frontend and backend during development

### Handoff condition
All services start cleanly with `docker-compose up` and health checks pass. Development environment ready for fraction lesson implementation.

---

## Agent 2: Database Schema & Migrations

### What it builds
Postgres schema for tracking student progress through the fraction equivalence lesson, storing lesson state, and managing simple user sessions for the math tutor.

### Step-by-step instructions
1. Create database schema with tables:
   - `students`: Basic student session tracking
   - `lessons`: Metadata for the fraction equivalence lesson
   - `lesson_progress`: Student progress through fraction lesson steps
   - `fraction_interactions`: Log of manipulative actions (combine, split, smash blocks)

2. Design `lesson_progress` table to track:
   - Current lesson step (exploration, guided_practice, assessment)
   - Fraction problems attempted and results
   - Time spent on fraction manipulative interactions

3. Create `fraction_interactions` table to log:
   - Action type (combine_blocks, split_block, smash_together)
   - Fraction values involved (numerator, denominator)
   - Success/failure of equivalence discovery

4. Write Alembic migration scripts for:
   - Initial schema creation
   - Sample data insertion (fraction equivalence lesson template)

5. Create database initialization script with sample lesson:
   - Lesson ID: "fraction-equivalence-1"
   - Steps: exploration, discovery, practice, assessment

### Verification checklist
- [ ] All tables created successfully with proper foreign key relationships
- [ ] Migration runs without errors in Docker container
- [ ] Sample lesson data loads correctly
- [ ] Can insert/query lesson progress records
- [ ] Database persists data between container restarts
- [ ] Fraction interaction logging captures manipulative actions

### Handoff condition
Database schema supports complete fraction lesson flow with progress tracking. Sample lesson data available for tutor conversation engine.

---

## Agent 3: Auth Layer

### What it builds
Simple JWT-based session management for anonymous student sessions during the fraction equivalence lesson, without requiring registration or login.

### Step-by-step instructions
1. Create FastAPI JWT utilities in `backend/auth/`:
   - Token generation for anonymous sessions
   - Token validation middleware
   - Session expiration (lesson duration + buffer)

2. Implement anonymous session creation:
   - Generate student session on first app load
   - Create JWT with student_id (UUID) and lesson_id
   - No password or email required

3. Create auth middleware for lesson API endpoints:
   - Validate JWT on lesson progress updates
   - Extract student_id for progress tracking
   - Handle token expiration gracefully

4. Frontend session management:
   - Store JWT in sessionStorage (not localStorage)
   - Auto-generate session on app initialization
   - Include token in API requests to lesson endpoints

5. Auth endpoints:
   - `POST /auth/session` - Create anonymous session
   - `POST /auth/refresh` - Refresh session token
   - No logout needed (session-based)

### Verification checklist
- [ ] Anonymous session created automatically on app load
- [ ] JWT token includes student_id and lesson_id claims
- [ ] Auth middleware validates tokens on lesson API calls
- [ ] Token refresh works before expiration
- [ ] Invalid/expired tokens return proper 401 responses
- [ ] Frontend handles auth errors gracefully

### Handoff condition
Working anonymous session system allows students to progress through fraction lesson with persistent progress tracking via JWT authentication.

---

## Agent 4: Backend API

### What it builds
FastAPI endpoints for the fraction equivalence lesson conversation engine, progress tracking, and manipulative interaction logging.

### Step-by-step instructions
1. Create lesson conversation API in `backend/lesson/`:
   - `GET /lesson/fraction-equivalence/start` - Initialize lesson
   - `POST /lesson/fraction-equivalence/response` - Process student response
   - `GET /lesson/fraction-equivalence/progress` - Get current lesson state

2. Implement scripted conversation engine:
   - Load conversation tree for fraction equivalence lesson
   - Handle branching logic for correct/incorrect fraction answers
   - Return next tutor message and expected response type

3. Create fraction manipulative API:
   - `POST /manipulative/action` - Log fraction block interactions
   - `GET /manipulative/state` - Get current workspace state
   - Actions: combine_blocks, split_block, check_equivalence

4. Build lesson progression logic:
   - Track progress through: exploration → discovery → practice → assessment
   - Validate fraction equivalence answers (1/2 = 2/4, etc.)
   - Determine when student can advance to next step

5. Implement conversation script responses:
   - Encouraging responses for correct fraction discoveries
   - Gentle hints for incorrect equivalence attempts
   - Warm, supportive tone matching Synthesis model

6. Create progress tracking endpoints:
   - Save lesson completion status
   - Track time spent on fraction manipulations
   - Store assessment results

### Verification checklist
- [ ] Lesson starts with proper exploration phase introduction
- [ ] Conversation engine responds correctly to fraction equivalence answers
- [ ] Manipulative actions logged with proper fraction values
- [ ] Student progress persists between session refreshes
- [ ] Assessment phase validates fraction equivalence correctly
- [ ] API handles invalid responses gracefully with helpful hints
- [ ] All endpoints return proper HTTP status codes

### Handoff condition
Complete backend supports full fraction lesson conversation flow with working manipulative interaction tracking and progress persistence.

---

## Agent 5: Frontend

### What it builds
Next.js web application optimized for iPad with chat-style tutor interface and interactive fraction manipulative workspace for teaching fraction equivalence.

### Step-by-step instructions
1. Create main lesson layout with two panels:
   - Left panel: Chat conversation with AI tutor
   - Right panel: Interactive fraction manipulative workspace

2. Build chat interface components:
   - Tutor message bubbles with warm, encouraging tone
   - Student response input (text and multiple choice)
   - Auto-scroll to latest conversation
   - iPad touch-optimized input controls

3. Implement interactive fraction manipulative:
   - Visual fraction blocks (rectangles divided into parts)
   - Drag-and-drop functionality for combining blocks
   - Split action to break blocks into smaller fractions
   - "Smash together" action to discover equivalences

4. Create fraction visualization system:
   - Display fractions as colored blocks (1/2, 1/4, 1/8, etc.)
   - Visual equivalence checking (overlay matching fractions)
   - Animated feedback when equivalences are discovered

5. Build lesson flow components:
   - Exploration phase: Free manipulation of fraction blocks
   - Discovery phase: Guided fraction equivalence exercises
   - Practice phase: Structured fraction problems
   - Assessment phase: Check for understanding quiz

6. Implement iPad-optimized interactions:
   - Touch-friendly button sizes (44px minimum)
   - Responsive design for iPad viewport
   - Gesture support for fraction manipulations
   - No hover states (touch-only interface)

7. Connect frontend to backend APIs:
   - Load lesson conversation from API
   - Send student responses to conversation engine
   - Log manipulative interactions in real-time
   - Save and restore lesson progress

### Verification checklist
- [ ] Chat interface displays tutor messages with proper formatting
- [ ] Fraction blocks render correctly and respond to touch
- [ ] Drag-and-drop works smoothly on iPad browser
- [ ] Equivalence discovery shows visual feedback animation
- [ ] Lesson progression follows correct sequence
- [ ] App loads and functions properly on iPad Safari
- [ ] Touch targets are appropriately sized for fingers
- [ ] Progress saves automatically during lesson
- [ ] Responsive layout works in both orientations

### Handoff condition
Fully functional iPad-optimized web app with working chat tutor and interactive fraction manipulative. Ready for testing on provided iPad device.

---

## Agent 6: Testing

### What it builds
Test suites validating the fraction equivalence lesson flow, manipulative interactions, and conversation logic for the math tutor prototype.

### Step-by-step instructions
1. Create backend API tests:
   - Test lesson initialization and conversation flow
   - Validate fraction equivalence checking logic (1/2 = 2/4 = 4/8)
   - Test manipulative action logging and state management
   - Verify progress tracking through lesson phases

2. Write conversation engine tests:
   - Test correct responses to fraction equivalence questions
   - Verify appropriate hints for incorrect answers
   - Test lesson progression logic (exploration → assessment)
   - Validate warm, encouraging tone in tutor responses

3. Create frontend component tests:
   - Test fraction block rendering and interactions
   - Verify drag-and-drop functionality works
   - Test chat interface message display
   - Validate iPad touch interaction handling

4. Build end-to-end lesson tests:
   - Complete fraction equivalence lesson walkthrough
   - Test session persistence across page refreshes
   - Verify lesson completion tracking
   - Test error handling for network issues

5. Create iPad-specific tests:
   - Touch interaction accuracy on fraction blocks
   - Responsive design validation
   - Performance testing on iPad Safari
   - Gesture recognition for manipulative actions

6. Set up test data:
   - Sample lesson conversation scripts
   - Test fraction equivalence problems
   - Mock student progress states

### Verification checklist
- [ ] All API endpoints return expected responses for fraction lesson
- [ ] Conversation logic handles correct/incorrect fraction answers
- [ ] Manipulative interactions log properly in database
- [ ] Frontend renders fraction blocks correctly
- [ ] End-to-end lesson completion works without errors
- [ ] Tests pass on iPad Safari browser
- [ ] Session persistence works across refreshes
- [ ] Error states display helpful messages

### Handoff condition
Comprehensive test coverage validates complete fraction lesson functionality. All tests pass for both desktop development and iPad target environment.

---

## Agent 7: Code Review

### What it builds
Code quality validation ensuring the fraction equivalence math tutor meets production standards and iPad optimization requirements.

### Step-by-step instructions
1. Review backend code structure:
   - FastAPI lesson conversation engine implementation
   - Database schema design for lesson progress tracking
   - JWT session management for anonymous students
   - Fraction equivalence validation logic accuracy

2. Audit frontend implementation:
   - Next.js component organization for chat and manipulative
   - iPad touch optimization and responsive design
   - State management for lesson progress
   - Accessibility considerations for educational content

3. Validate conversation script quality:
   - Warm, encouraging tutor tone matching Synthesis model
   - Appropriate scaffolding for fraction concept learning
   - Clear progression through exploration to assessment
   - Helpful hints for common fraction misconceptions

4. Review fraction manipulative design:
   - Intuitive drag-and-drop interactions
   - Clear visual representation of fraction equivalence
   - Appropriate feedback for fraction discoveries
   - Age-appropriate complexity for elementary students

5. Check Docker and deployment setup:
   - Clean docker-compose configuration
   - Proper environment variable management
   - Build optimization for production deployment
   - Database migration reliability

6. Security and performance review:
   - JWT implementation security
   - API endpoint validation
   - Frontend performance on iPad
   - Memory usage during lesson interactions

### Verification checklist
- [ ] Code follows project conventions and is well-documented
- [ ] Fraction equivalence logic is mathematically correct
- [ ] Chat interface provides appropriate educational scaffolding
- [ ] Manipulative interactions are intuitive for children
- [ ] iPad optimization meets touch interface standards
- [ ] No security vulnerabilities in auth implementation
- [ ] Database queries are efficient and indexed
- [ ] Error handling provides helpful user feedback
- [ ] Code is maintainable for future lesson additions

### Handoff condition
Code quality meets production standards with excellent user experience for fraction learning. Ready for final documentation and demo preparation.

---

## Agent 8: Documentation

### What it builds
Complete documentation package for the Synthesis math tutor clone, including setup instructions, demo video, and technical architecture overview.

### Step-by-step instructions
1. Create comprehensive README.md:
   - Project overview and fraction equivalence lesson scope
   - Quick start with `docker-compose up` instructions
   - iPad testing setup and browser requirements
   - Architecture overview of chat + manipulative design

2. Document lesson conversation flow:
   - Exploration phase: Free fraction block manipulation
   - Discovery phase: Guided equivalence exercises (1/2 = 2/4)
   - Practice phase: Structured fraction problems
   - Assessment phase: Check for understanding quiz

3. Create technical documentation:
   - API endpoint documentation for lesson progression
   - Database schema explanation for progress tracking
   - Frontend component structure for chat and manipulative
   - Deployment guide for production use

4. Record 1-2 minute demo video:
   - Show complete fraction lesson walkthrough
   - Demonstrate chat conversation with tutor
   - Highlight fraction block manipulations and equivalence discovery
   - Capture iPad interaction showing touch responsiveness

5. Write architectural decisions document:
   - Technology stack choices (Next.js, FastAPI, Postgres)
   - Monorepo structure rationale
   - iPad optimization approach
   - Conversation scripting vs. LLM decision

6. Create troubleshooting guide:
   - Common Docker setup issues
   - iPad browser compatibility notes
   - Database connection debugging
   - Frontend development tips

### Verification checklist
- [ ] README provides clear setup instructions that work from scratch
- [ ] Demo video shows complete lesson functionality
- [ ] Technical docs explain all major components
- [ ] Video demonstrates iPad touch interactions clearly
- [ ] Documentation explains fraction equivalence teaching approach
- [ ] Setup guide works for new developers
- [ ] Architecture decisions are well-justified
- [ ] Demo shows the "magical" learning experience goal

### Handoff condition
Complete documentation package ready for stakeholder review. Demo video showcases working fraction equivalence lesson with conversational AI tutor and interactive manipulative on iPad.