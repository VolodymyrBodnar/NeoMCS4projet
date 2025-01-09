"""Add created and updated at to booking

Revision ID: 887f2c80e0ae
Revises: c8a29c5a3564
Create Date: 2025-01-09 21:45:59.783022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '887f2c80e0ae'
down_revision: Union[str, None] = 'c8a29c5a3564'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('bookings', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'updated_at')
    op.drop_column('bookings', 'created_at')
    # ### end Alembic commands ###
