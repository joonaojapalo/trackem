"""empty message

Revision ID: baf14df5c20b
Revises: ce79c48e8188
Create Date: 2016-03-04 14:00:37.220000

"""

# revision identifiers, used by Alembic.
revision = 'baf14df5c20b'
down_revision = 'ce79c48e8188'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_group', 'id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_group', sa.Column('id', sa.INTEGER(), nullable=False))
    ### end Alembic commands ###
