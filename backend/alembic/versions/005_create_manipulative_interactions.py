"""Create manipulative_interactions table

Revision ID: 005_create_manipulative_interactions
Revises: 004_create_user_sessions
Create Date: 2025-03-13 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '005_create_manipulative_interactions'
down_revision = '004_create_user_sessions'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'manipulative_interactions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('session_id', UUID(as_uuid=True), nullable=False),
        sa.Column('step_id', UUID(as_uuid=True), nullable=False),
        sa.Column('interaction_type', sa.String(50), nullable=False),
        sa.Column('fraction_value', sa.String(20), nullable=False),
        sa.Column('position_x', sa.Integer(), nullable=True),
        sa.Column('position_y', sa.Integer(), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())")),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())")),
        sa.ForeignKeyConstraint(['session_id'], ['user_sessions.id'], name='fk_manipulative_interactions_user_sessions'),
        sa.ForeignKeyConstraint(['step_id'], ['lesson_steps.id'], name='fk_manipulative_interactions_lesson_steps')
    )


def downgrade() -> None:
    op.drop_table('manipulative_interactions')
