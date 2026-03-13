"""003_create_lesson_steps

Revision ID: 511f893ae351
Revises: 5db4c8780ace
Create Date: 2026-03-13 05:00:52.761809

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '511f893ae351'
down_revision = '5db4c8780ace'
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
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE', name='fk_lesson_steps_lessons')
    )


def downgrade() -> None:
    op.drop_table('lesson_steps')
