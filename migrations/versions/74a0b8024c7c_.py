"""empty message

Revision ID: 74a0b8024c7c
Revises: ee6b7b2e6a16
Create Date: 2016-03-01 13:04:23.873000

"""

# revision identifiers, used by Alembic.
revision = '74a0b8024c7c'
down_revision = 'ee6b7b2e6a16'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'name')
    ### end Alembic commands ###
