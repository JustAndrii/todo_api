"""initial schema

Revision ID: a2e986748e3c
Revises:
Create Date: 2026-10-20 20:43:38.375776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2e986748e3c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created',sa.DateTime(),nullable=True)
    )

    op.create_table(
        'tasks',
        sa.Column('id',sa.Integer(),primary_key=True),
        sa.Column('title',sa.String(),nullable=False),
        sa.Column('completed',sa.Boolean(), nullable=False),
        sa.Column('user_id',sa.Integer(),sa.ForeignKey('users.id'))
    )


def downgrade() -> None:
    op.drop_table('tasks')
    op.drop_table('users')
