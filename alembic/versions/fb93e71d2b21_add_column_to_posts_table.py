"""add column to posts table

Revision ID: fb93e71d2b21
Revises: 8cd633c75258
Create Date: 2024-12-27 09:10:21.304061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb93e71d2b21'
down_revision: Union[str, None] = '8cd633c75258'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(table_name="posts", column=sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column(table_name="posts", column_name="content")
    pass
