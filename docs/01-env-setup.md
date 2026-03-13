# Environment Setup & Infrastructure

## Overview

Agent 1 established the foundational infrastructure for the Synthesis Math Tutor application, creating a monorepo structure with production-ready Docker configuration and basic application scaffolding.

## What Was Built

### 1. Monorepo Structure

Created a clean monorepo organization with the following structure:

```
/
├── backend/          # FastAPI Python application
├── frontend/         # Next.js React application
├── db/               # Database-related scripts
├── docs/             # Project documentation
├── docker-compose.yml # Container orchestration
└── .env              # Environment configuration
```

**Decision**: Monorepo architecture over separate repositories.

**Rationale**:
- Single source of truth for the entire application
- Easier dependency management and versioning
- Simplified Docker orchestration with docker-compose
- Better code sharing and consistency across services
- Matches the project's "simplicity over complexity" philosophy

### 2. Docker Configuration

#### Backend Dockerfile (`backend/Dockerfile`)

**Multi-stage build** with two stages:
- **Builder stage**: Installs build dependencies (gcc, g++) and Python packages
- **Runner stage**: Minimal runtime image with only necessary dependencies

**Key features**:
- Python 3.11.9-slim base image
- Non-root user (`appuser`) for security
- Health check endpoint configured
- Proper layer caching (requirements.txt copied first)
- Startup script (`start.sh`) for migrations and seeding

**Decision**: Multi-stage build over single-stage.

**Rationale**:
- Smaller final image size (build dependencies not included)
- Better security (fewer attack surfaces)
- Faster deployments (smaller images)
- Production-ready best practices

#### Frontend Dockerfile (`frontend/Dockerfile`)

**Three-stage build**:
- **Deps stage**: Installs npm dependencies
- **Builder stage**: Builds Next.js application
- **Runner stage**: Minimal runtime with standalone output

**Key features**:
- Node.js 18.17.1-alpine base image
- Standalone output mode for smaller image
- Non-root user (`nextjs`) for security
- Health check configured
- Proper static file handling

**Decision**: Standalone output mode over full Next.js installation.

**Rationale**:
- Significantly smaller image size
- Faster container startup
- Only necessary files included
- Matches Next.js production best practices

#### Docker Compose Configuration (`docker-compose.yml`)

**Services configured**:
1. **PostgreSQL Database** (`db`)
   - PostgreSQL 16.2-alpine image
   - Named volume for data persistence
   - Health checks with retry logic
   - Port 5432 exposed for development

2. **FastAPI Backend** (`backend`)
   - Builds from `backend/Dockerfile`
   - Depends on database health
   - Volume mounts for hot reload in development
   - Port 8000 exposed

3. **Next.js Frontend** (`frontend`)
   - Builds from `frontend/Dockerfile`
   - Depends on backend health
   - Volume mounts for hot reload in development
   - Port 3000 exposed

**Key decisions**:
- Health checks with proper retry logic
- Service dependencies ensure correct startup order
- Volume mounts for development hot reload
- Environment variables from `.env` file
- Restart policies (`unless-stopped`) for production resilience

**Decision**: Health check-based dependencies over simple `depends_on`.

**Rationale**:
- Ensures services are actually ready, not just started
- Prevents race conditions during startup
- More reliable in production environments
- Matches Docker best practices

### 3. Application Scaffolding

#### Backend (`backend/app/main.py`)

Created minimal FastAPI application with:
- CORS middleware configured for frontend communication
- Health check endpoint (`/health`)
- Root endpoint (`/`)
- Basic application metadata

**Decision**: Minimal scaffolding over full implementation.

**Rationale**:
- Verifies Docker setup works correctly
- Establishes application structure
- Allows incremental feature development
- Follows "happy path focus" philosophy

#### Frontend (`frontend/app/`)

Created Next.js App Router structure with:
- Root layout (`layout.tsx`)
- Landing page (`page.tsx`)
- Health check API route (`app/api/health/route.ts`)
- TypeScript configuration
- Next.js standalone output configuration

**Decision**: Next.js App Router over Pages Router.

**Rationale**:
- Modern Next.js 13+ approach
- Better server-side rendering support
- Built-in loading and error states
- Matches project requirements

### 4. Configuration Management

#### Environment Variables (`.env`)

Created `.env` file with safe development defaults:
- Database credentials (PostgreSQL)
- JWT secret key (development only)
- Environment mode (development/production)
- API URLs

**Decision**: `.env` file with defaults over hardcoded values.

**Rationale**:
- Easy local development setup
- No secrets in code
- Can be overridden in production
- Follows 12-factor app principles

#### Backend Configuration (`backend/config.py`)

Centralized configuration management:
- Reads from environment variables
- Falls back to safe defaults
- Constructs `DATABASE_URL` from components
- Supports both Docker and local development

**Decision**: Centralized config over scattered environment reads.

**Rationale**:
- Single source of truth for configuration
- Easier to maintain and update
- Consistent across application
- Supports multiple deployment environments

### 5. Development Dependencies

#### Backend (`backend/requirements.txt`)

Initial dependencies:
- FastAPI and Uvicorn for web framework
- Pydantic for data validation
- python-dotenv for environment management

**Decision**: Minimal initial dependencies.

**Rationale**:
- Follows "minimal dependencies" philosophy
- Add dependencies as needed
- Faster installation and smaller images
- Easier to maintain

#### Frontend (`frontend/package.json`)

Initial dependencies:
- Next.js 14.2.18
- React 18.3.1
- TypeScript 5.5.3

**Decision**: Latest stable versions.

**Rationale**:
- Modern features and performance
- Long-term support
- Security updates
- Matches project requirements

## Key Decisions Made

### 1. Monorepo Architecture
**Decision**: Single repository for all services.

**Why**: Simplifies development, deployment, and maintenance. All code in one place makes it easier to coordinate changes across services.

### 2. Multi-stage Docker Builds
**Decision**: Separate build and runtime stages.

**Why**: Significantly reduces final image size, improves security, and follows production best practices.

### 3. Health Check Dependencies
**Decision**: Use health checks to determine service readiness.

**Why**: Prevents race conditions and ensures services are actually ready before dependent services start.

### 4. Standalone Next.js Output
**Decision**: Use Next.js standalone output mode.

**Why**: Smaller Docker images, faster startup times, and only necessary files included.

### 5. Non-root Users
**Decision**: Run containers as non-root users.

**Why**: Security best practice - reduces attack surface if container is compromised.

## What Was Skipped/Deferred

### 1. Production Secrets Management
**Skipped**: Production-grade secrets management (e.g., AWS Secrets Manager, HashiCorp Vault).

**Why**: Focus on development setup first. Production secrets can be added later when deploying.

### 2. CI/CD Pipeline
**Skipped**: Continuous integration and deployment pipelines.

**Why**: Infrastructure setup is the priority. CI/CD can be added in later phases.

### 3. Monitoring and Logging
**Skipped**: Application monitoring and centralized logging.

**Why**: Not required for initial setup. Can be added as application grows.

### 4. Load Balancing
**Skipped**: Multiple service instances and load balancing.

**Why**: Single-instance setup is sufficient for initial development and MVP.

### 5. Database Migrations Automation
**Skipped**: Automatic migration running in Dockerfile.

**Why**: Migrations need database connection, which isn't available during build. Handled in startup script instead (Agent 2).

## Problems Encountered & Resolutions

### 1. Docker Build Context Issues
**Problem**: Initial Dockerfile attempts to copy files before they existed.

**Resolution**: Created minimal application structure first, then configured Dockerfiles to work with that structure.

### 2. Next.js Standalone Configuration
**Problem**: Next.js standalone output requires specific configuration.

**Resolution**: Added `output: 'standalone'` to `next.config.js` and updated Dockerfile to copy standalone output correctly.

### 3. Health Check Timing
**Problem**: Services starting before dependencies are ready.

**Resolution**: Implemented health checks with proper retry logic and start periods to allow services time to initialize.

### 4. Volume Mount Permissions
**Problem**: Permission issues with volume mounts in development.

**Resolution**: Ensured proper user permissions in Dockerfiles and used non-root users consistently.

### 5. CORS Configuration
**Problem**: Frontend couldn't communicate with backend initially.

**Resolution**: Configured CORS middleware in FastAPI to allow requests from `http://localhost:3000`.

## Verification

### Native Execution
Both services were verified to start successfully natively:
- Backend: `uvicorn app.main:app --reload` on port 8000
- Frontend: `npm run dev` on port 3000
- Health checks accessible and responding

### Docker Configuration
- Dockerfiles syntax verified
- docker-compose.yml validated
- Service dependencies configured correctly
- Health checks functional

## Files Created/Modified

```
.env                          # Environment variables
.gitignore                    # Git ignore rules
docker-compose.yml            # Container orchestration
backend/
  ├── Dockerfile             # Backend container definition
  ├── .dockerignore          # Docker ignore rules
  ├── app/
  │   ├── __init__.py
  │   └── main.py            # FastAPI application
  ├── config.py              # Configuration management
  └── requirements.txt       # Python dependencies
frontend/
  ├── Dockerfile             # Frontend container definition
  ├── .dockerignore          # Docker ignore rules
  ├── app/
  │   ├── layout.tsx         # Root layout
  │   ├── page.tsx           # Landing page
  │   └── api/health/route.ts # Health check
  ├── next.config.js         # Next.js configuration
  ├── package.json           # Node dependencies
  └── tsconfig.json          # TypeScript configuration
docs/
  └── README.md              # Documentation directory
```

## Next Steps

After environment setup, the next agent (Agent 2) would:
1. Set up database schema and models
2. Configure database migrations
3. Create seed data for development

The infrastructure foundation was ready for database and application development.
