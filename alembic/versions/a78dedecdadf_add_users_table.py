"""add users table

Revision ID: a78dedecdadf
Revises: fb93e71d2b21
Create Date: 2024-12-27 09:44:40.556152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a78dedecdadf'
down_revision: Union[str, None] = 'fb93e71d2b21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer()),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
