"""create posts table

Revision ID: 8cd633c75258
Revises: 
Create Date: 2024-12-27 08:50:58.804549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cd633c75258'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    pass
