"""006_create_conversation_logs

Revision ID: 8a05ecc47544
Revises: 34966085bd2d
Create Date: 2026-03-13 05:00:54.537107

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '8a05ecc47544'
down_revision = '34966085bd2d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'conversation_logs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('session_id', UUID(as_uuid=True), nullable=False),
        sa.Column('step_id', UUID(as_uuid=True), nullable=False),
        sa.Column('speaker', sa.String(20), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(50), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())")),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text("TIMEZONE('utc', NOW())")),
        sa.ForeignKeyConstraint(['session_id'], ['user_sessions.id'], ondelete='CASCADE', name='fk_conversation_logs_user_sessions'),
        sa.ForeignKeyConstraint(['step_id'], ['lesson_steps.id'], ondelete='CASCADE', name='fk_conversation_logs_lesson_steps')
    )


def downgrade() -> None:
    op.drop_table('conversation_logs')
