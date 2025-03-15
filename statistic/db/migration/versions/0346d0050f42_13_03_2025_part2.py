"""13.03.2025 part2

Revision ID: 0346d0050f42
Revises: dd2424f51731
Create Date: 2025-03-13 14:49:23.614872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0346d0050f42'
down_revision: Union[str, None] = 'dd2424f51731'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('statistics_book_instance_id_key', 'statistics', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('statistics_book_instance_id_key', 'statistics', ['book_instance_id'])
    # ### end Alembic commands ###
