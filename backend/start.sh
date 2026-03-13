#!/bin/bash
set -e

echo "Waiting for database to be ready..."
# Docker compose healthcheck ensures db is ready, but give it a moment
sleep 3

echo "Running Alembic migrations..."
cd /app
alembic upgrade head || echo "Migration failed or already applied"

echo "Running seed script..."
python /app/../db/seed.py || echo "Seed script failed or data already exists"

echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
