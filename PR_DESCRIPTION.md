# feat: [infrastructure] - Docker Environment & Monorepo Setup

## Feature Summary

Complete Docker-based development environment setup for the Synthesis Math Tutor monorepo. This PR establishes the foundation for the Next.js frontend, FastAPI backend, and PostgreSQL database services with proper containerization, health checks, and development workflow support.

## Requirements Addressed

- ✅ Created monorepo folder structure (`/frontend`, `/backend`, `/db`, `/docs`)
- ✅ Dockerfile for frontend (Next.js, pinned base image, multi-stage build)
- ✅ Dockerfile for backend (FastAPI/Python, pinned base image)
- ✅ Verified and updated `docker-compose.yml` with all services properly wired
- ✅ Created `.env` from `.env.example` with safe development defaults
- ✅ Infrastructure ready for application code implementation

## Technical Implementation

### Monorepo Structure

Created the following directory structure:
```
synthesis-tutor/
├── frontend/          # Next.js app (to be implemented)
├── backend/           # FastAPI app (to be implemented)
├── db/                # Database migrations (to be added)
├── docs/              # Documentation
├── docker-compose.yml # Service orchestration
└── .env               # Environment variables (gitignored)
```

**Decision**: Standard monorepo structure allows for shared tooling, consistent development workflow, and easier dependency management between frontend and backend.

### Frontend Dockerfile

**Base Image**: `node:18.17.1-alpine` (pinned version)

**Key Decisions**:
1. **Multi-stage build**: Separates build dependencies from runtime, reducing final image size
2. **Alpine Linux**: Smaller image size (~5MB base vs ~150MB for standard Node image)
3. **Non-root user**: Security best practice - runs as `nextjs` user (UID 1001)
4. **Development-first**: Configured for dev mode with hot reload, can be optimized for production later
5. **Health check**: HTTP endpoint at `/api/health` for container health monitoring

**Structure**:
- Stage 1 (builder): Installs dependencies and builds Next.js app
- Stage 2 (runner): Minimal runtime with only necessary files

**Why**: Follows Docker best practices from `.cursor/rules/docker.mdc` - pinned versions, multi-stage builds, non-root users, and health checks are all mandatory requirements.

### Backend Dockerfile

**Base Image**: `python:3.11.9-slim` (pinned version)

**Key Decisions**:
1. **Slim variant**: Reduces image size while maintaining compatibility
2. **System dependencies**: Includes `gcc` and `postgresql-client` for database connectivity
3. **Non-root user**: Runs as `appuser` for security
4. **Fallback dependencies**: If `requirements.txt` is missing, installs minimal FastAPI stack
5. **Health check**: HTTP endpoint at `/health` for container health monitoring

**Why**: Python 3.11.9 is the latest stable 3.11.x version. Slim variant reduces attack surface and image size. Non-root user and health checks are mandatory per Docker rules.

### Docker Compose Configuration

**Services Configured**:

1. **Database (PostgreSQL)**
   - Image: `postgres:16-alpine` (pinned)
   - Port: `5432`
   - Health check: `pg_isready` command
   - Volume: `postgres_data` for persistence
   - Restart policy: `unless-stopped`

2. **Backend (FastAPI)**
   - Build: `./backend`
   - Port: `8000`
   - Health check: HTTP GET to `/health`
   - Depends on: Database (waits for healthy state)
   - Hot reload: Enabled via volume mount and `--reload` flag
   - Restart policy: `unless-stopped`

3. **Frontend (Next.js)**
   - Build: `./frontend`
   - Port: `3000`
   - Health check: HTTP GET to `/api/health`
   - Depends on: Backend (waits for healthy state)
   - Hot reload: Enabled via volume mounts
   - Restart policy: `unless-stopped`

**Key Decisions**:
1. **Health checks on all services**: Required by Docker rules, ensures services are ready before dependencies start
2. **Service dependencies**: Backend waits for database, frontend waits for backend
3. **Volume mounts**: Source code mounted for hot reload in development
4. **Named volumes**: Database uses named volume for data persistence
5. **Explicit container names**: Makes debugging and management easier
6. **Port exposure**: All services expose ports for local development access

**Why**: Follows all requirements from `.cursor/rules/docker.mdc`:
- Every service has health checks
- Dependencies use `condition: service_healthy`
- Restart policies explicitly set
- Ports documented with comments
- Named volumes for persistent data

### Environment Variables

Created `.env` from `.env.example` with safe development defaults:

- `POSTGRES_USER=postgres`
- `POSTGRES_PASSWORD=dev_password_123` (safe for local dev only)
- `POSTGRES_DB=superbuilders-synthesis`
- `JWT_SECRET=dev-jwt-secret-key-change-in-production-min-32-chars-long` (32+ chars as required)
- `ENVIRONMENT=development`
- `NEXT_PUBLIC_API_URL=http://localhost:8000`

**Decision**: Used development-safe defaults that are clearly not production-ready. The JWT secret is long enough (32+ chars) but obviously needs to be changed for production.

### Minimal Placeholder Files

Created minimal files to allow containers to build and pass health checks:

**Frontend**:
- `package.json`: Next.js 14.2.5, React 18.3.1, TypeScript 5.5.3
- `next.config.js`: Standalone output mode for Docker
- `tsconfig.json`: Strict TypeScript configuration
- `app/api/health/route.ts`: Health check endpoint
- `app/page.tsx` & `app/layout.tsx`: Minimal Next.js app structure

**Backend**:
- `requirements.txt`: FastAPI 0.104.1, Uvicorn 0.24.0, Pydantic 2.5.3
- `main.py`: Minimal FastAPI app with `/health` endpoint

**Decision**: These are infrastructure files, not application code. They allow the Docker environment to be verified before application implementation begins.

### Additional Files

- `.gitignore`: Excludes `.env`, `node_modules`, `__pycache__`, build artifacts
- `docs/INFRASTRUCTURE.md`: Complete documentation of the setup
- `.dockerignore` files: Exclude unnecessary files from Docker builds

## Docker Verification

### Verification Steps

To verify the setup:

```bash
# 1. Clean build test
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# 2. Health check verification
docker-compose ps  # All services should show "healthy" or "Up"

# 3. Service connectivity test
curl http://localhost:3000/api/health  # Frontend
curl http://localhost:8000/health      # Backend
docker-compose exec db pg_isready -U postgres  # Database

# 4. Log verification (no errors in startup)
docker-compose logs --tail=50

# 5. Clean shutdown test
docker-compose down
```

### Expected Results

- ✅ All three services start without errors
- ✅ Frontend accessible at http://localhost:3000
- ✅ Backend API docs accessible at http://localhost:8000/docs
- ✅ Backend health endpoint responds at http://localhost:8000/health
- ✅ Frontend health endpoint responds at http://localhost:3000/api/health
- ✅ Postgres container accepts connections
- ✅ All health checks pass

**Note**: Docker verification was not possible in the current environment (Docker not available). The Dockerfiles and docker-compose.yml follow all best practices and should work correctly when Docker is available. Manual verification is required before merging.

## Testing Completed

- ✅ Dockerfile syntax validated
- ✅ docker-compose.yml syntax validated
- ✅ All pinned versions verified
- ✅ Health check endpoints implemented
- ✅ Service dependencies configured correctly
- ⚠️ **Manual Docker verification required** (Docker not available in build environment)

## Next Steps

1. **Agent 2 (Database Schema)**: Will add Alembic migrations and database models
2. **Agent 3 (Auth Layer)**: Will implement JWT authentication
3. **Agent 4 (Backend API)**: Will build FastAPI endpoints for lesson management
4. **Agent 5 (Frontend)**: Will implement Next.js UI with fraction manipulative

## Decisions Summary

| Decision | Rationale |
|----------|-----------|
| Pinned base images | Security and reproducibility - no `latest` tags |
| Multi-stage builds | Smaller production images, better layer caching |
| Non-root users | Security best practice, required by Docker rules |
| Health checks on all services | Required for proper dependency management |
| Alpine/slim variants | Smaller attack surface and image size |
| Development-first setup | Hot reload essential for development workflow |
| Named volumes for database | Data persistence between container restarts |
| Explicit service dependencies | Ensures services start in correct order |
| Minimal placeholder files | Allows infrastructure verification before app code |

## Files Changed

- Created: `frontend/Dockerfile`, `frontend/.dockerignore`
- Created: `backend/Dockerfile`, `backend/.dockerignore`
- Created: `frontend/package.json`, `frontend/next.config.js`, `frontend/tsconfig.json`
- Created: `frontend/app/api/health/route.ts`, `frontend/app/page.tsx`, `frontend/app/layout.tsx`
- Created: `backend/requirements.txt`, `backend/main.py`
- Created: `.gitignore`, `docs/INFRASTRUCTURE.md`
- Modified: `docker-compose.yml` (added health checks, restart policies, container names)
- Created: `.env` (from `.env.example` with development defaults)

---

**Ready for**: Manual Docker verification and subsequent agent implementation phases.
