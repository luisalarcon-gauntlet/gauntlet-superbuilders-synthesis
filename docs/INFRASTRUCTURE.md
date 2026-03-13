# Infrastructure Setup

This document describes the Docker-based development environment for the Synthesis Math Tutor application.

## Monorepo Structure

```
synthesis-tutor/
├── frontend/          # Next.js app with fraction manipulative UI
├── backend/           # FastAPI for lesson progress tracking
├── db/                # Database migrations and seeds (to be added)
├── docs/              # Documentation
├── docker-compose.yml # Services: frontend, backend, postgres
└── .env               # Environment variables (not in git)
```

## Services

### Database (PostgreSQL)
- **Image**: `postgres:16-alpine` (pinned version)
- **Port**: `5432`
- **Volume**: `postgres_data` (persistent storage)
- **Health Check**: Uses `pg_isready` command

### Backend (FastAPI)
- **Base Image**: `python:3.11.9-slim` (pinned version)
- **Port**: `8000`
- **Health Endpoint**: `/health`
- **Features**:
  - Non-root user execution
  - Hot reload enabled in development
  - Health checks configured

### Frontend (Next.js)
- **Base Image**: `node:18.17.1-alpine` (pinned version)
- **Port**: `3000`
- **Health Endpoint**: `/api/health`
- **Features**:
  - Multi-stage build
  - Non-root user execution
  - Development mode with hot reload
  - iPad-optimized for touch interactions

## Getting Started

1. **Copy environment variables**:
   ```bash
   cp .env.example .env
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Verify services are healthy**:
   ```bash
   docker-compose ps
   ```

4. **Access services**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend Docs: http://localhost:8000/docs
   - Database: localhost:5432

## Environment Variables

See `.env.example` for required variables:
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `JWT_SECRET`: Secret key for JWT tokens
- `ENVIRONMENT`: `development` or `production`
- `NEXT_PUBLIC_API_URL`: Backend API URL for frontend

## Development Workflow

- **Hot Reload**: Both frontend and backend support hot reload in development
- **Volume Mounts**: Source code is mounted as volumes for live updates
- **Database Persistence**: Data persists in Docker volumes between restarts

## Health Checks

All services include health checks:
- Database: Checks PostgreSQL readiness
- Backend: HTTP GET to `/health`
- Frontend: HTTP GET to `/api/health`

Services wait for dependencies to be healthy before starting.
