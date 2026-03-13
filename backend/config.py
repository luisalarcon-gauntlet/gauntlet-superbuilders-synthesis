"""
Application configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "dev_password_123")
POSTGRES_DB = os.getenv("POSTGRES_DB", "synthesis_tutor_dev")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "dev_jwt_secret_key_change_in_production_12345678901234567890")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
