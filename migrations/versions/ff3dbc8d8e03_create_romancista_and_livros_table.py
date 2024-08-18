"""create romancista and livros table

Revision ID: ff3dbc8d8e03
Revises: 7b1d9d83a96d
Create Date: 2024-08-17 22:48:18.388922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff3dbc8d8e03'
down_revision: Union[str, None] = '7b1d9d83a96d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('romancistas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('livros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ano', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.Column('romancista_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['romancista_id'], ['romancistas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('livros')
    op.drop_table('romancistas')
    # ### end Alembic commands ###
