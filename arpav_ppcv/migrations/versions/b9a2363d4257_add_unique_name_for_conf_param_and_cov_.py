"""add unique name for conf param and cov conf

Revision ID: b9a2363d4257
Revises: c9a3edc651d2
Create Date: 2024-05-04 22:36:54.203672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b9a2363d4257'
down_revision: Union[str, None] = 'c9a3edc651d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_configurationparameter_name'), 'configurationparameter', ['name'], unique=True)
    op.add_column('coverageconfiguration', sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_index(op.f('ix_coverageconfiguration_name'), 'coverageconfiguration', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_coverageconfiguration_name'), table_name='coverageconfiguration')
    op.drop_column('coverageconfiguration', 'name')
    op.drop_index(op.f('ix_configurationparameter_name'), table_name='configurationparameter')
    # ### end Alembic commands ###
