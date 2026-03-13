#!/bin/bash
set -e

echo "Starting backend service..."

# Run migrations
echo "Running database migrations..."
python run_migrations.py

# Run seed script (idempotent, safe to run multiple times)
echo "Seeding database..."
python db/seed.py || echo "Seed script completed (may have skipped existing data)"

# Start the application
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
