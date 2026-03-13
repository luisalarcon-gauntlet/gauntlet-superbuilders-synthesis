"""Create lesson_steps table

Revision ID: 003_create_lesson_steps
Revises: 002_create_lessons
Create Date: 2025-03-13 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '003_create_lesson_steps'
down_revision = '002_create_lessons'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'lesson_steps',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('lesson_id', UUID(as_uuid=True), nullable=False),
        sa.Column('step_number', sa.Integer(), nullable=False),
        sa.Column('step_type', sa.String(50), nullable=False),
        sa.Column('tutor_message', sa.Text(), nullable=False),
        sa.Column('expected_action', sa.String(100), nullable=True),
        sa.Column('success_message', sa.Text(), nullable=True),
        sa.Column('hint_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())")),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())")),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], name='fk_lesson_steps_lessons')
    )


def downgrade() -> None:
    op.drop_table('lesson_steps')
