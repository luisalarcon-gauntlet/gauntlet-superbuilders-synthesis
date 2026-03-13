"""Create lessons table

Revision ID: 002_create_lessons
Revises: 001_create_users
Create Date: 2025-03-13 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '002_create_lessons'
down_revision = '001_create_users'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'lessons',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('topic', sa.String(100), nullable=False),
        sa.Column('difficulty_level', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())")),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())"))
    )


def downgrade() -> None:
    op.drop_table('lessons')
