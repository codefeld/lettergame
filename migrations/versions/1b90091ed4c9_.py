"""empty message

Revision ID: 1b90091ed4c9
Revises: ac284300a1ef
Create Date: 2022-08-14 11:36:23.273823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b90091ed4c9'
down_revision = 'ac284300a1ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('parent_key', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'parent_key')
    # ### end Alembic commands ###
