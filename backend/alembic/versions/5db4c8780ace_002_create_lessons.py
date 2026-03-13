"""002_create_lessons

Revision ID: 5db4c8780ace
Revises: b3bf18e96343
Create Date: 2026-03-13 05:00:52.173089

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '5db4c8780ace'
down_revision = 'b3bf18e96343'
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
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())")),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())"))
    )


def downgrade() -> None:
    op.drop_table('lessons')
