"""empty message

Revision ID: 0a90354a883f
Revises: c73d0415e911
Create Date: 2022-07-17 19:36:43.391135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a90354a883f'
down_revision = 'c73d0415e911'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('clues', sa.PickleType(), nullable=True))
    op.alter_column('games', 'word',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('games', 'key',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.create_unique_constraint(None, 'games', ['key'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'games', type_='unique')
    op.alter_column('games', 'key',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('games', 'word',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_column('games', 'clues')
    # ### end Alembic commands ###
