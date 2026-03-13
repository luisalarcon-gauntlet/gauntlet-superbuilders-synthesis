"""007_add_auth_fields_to_users

Revision ID: a1b2c3d4e5f6
Revises: 8a05ecc47544
Create Date: 2026-03-13 05:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '8a05ecc47544'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add email and password_hash columns to users table
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('password_hash', sa.String(255), nullable=True))
    
    # Make email and password_hash NOT NULL after adding them
    # First, we need to populate existing rows with dummy data
    op.execute("UPDATE users SET email = 'user_' || id::text || '@example.com' WHERE email IS NULL")
    op.execute("UPDATE users SET password_hash = 'dummy_hash' WHERE password_hash IS NULL")
    
    # Now make them NOT NULL
    op.alter_column('users', 'email', nullable=False)
    op.alter_column('users', 'password_hash', nullable=False)
    
    # Create unique index on email
    op.create_index('ix_users_email', 'users', ['email'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email')
