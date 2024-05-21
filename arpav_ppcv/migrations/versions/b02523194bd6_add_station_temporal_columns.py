"""add station temporal columns

Revision ID: b02523194bd6
Revises: b9a2363d4257
Create Date: 2024-05-07 15:06:56.860040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b02523194bd6'
down_revision: Union[str, None] = 'b9a2363d4257'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('station', sa.Column('active_since', sa.Date(), nullable=True))
    op.add_column('station', sa.Column('active_until', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('station', 'active_until')
    op.drop_column('station', 'active_since')
    # ### end Alembic commands ###