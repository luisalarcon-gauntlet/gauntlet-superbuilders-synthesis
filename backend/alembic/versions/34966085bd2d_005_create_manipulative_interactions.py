"""005_create_manipulative_interactions

Revision ID: 34966085bd2d
Revises: 8ecb14618567
Create Date: 2026-03-13 05:00:53.877432

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '34966085bd2d'
down_revision = '8ecb14618567'
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
        sa.ForeignKeyConstraint(['session_id'], ['user_sessions.id'], ondelete='CASCADE', name='fk_manipulative_interactions_user_sessions'),
        sa.ForeignKeyConstraint(['step_id'], ['lesson_steps.id'], ondelete='CASCADE', name='fk_manipulative_interactions_lesson_steps')
    )


def downgrade() -> None:
    op.drop_table('manipulative_interactions')
