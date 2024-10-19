"""added task id to event so it can get updated or canceled

Revision ID: 4143ac6bd9e4
Revises: 66343a35c8fc
Create Date: 2024-10-19 00:49:12.909894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4143ac6bd9e4'
down_revision: Union[str, None] = '66343a35c8fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('task_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'task_id')
    # ### end Alembic commands ###