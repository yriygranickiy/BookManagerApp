"""13.03.2025

Revision ID: dd2424f51731
Revises: 6cb6e1027146
Create Date: 2025-03-13 14:03:24.288645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd2424f51731'
down_revision: Union[str, None] = '6cb6e1027146'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('statistics', sa.Column('username', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('statistics', 'username')
    # ### end Alembic commands ###
