"""empty message

Revision ID: ee6b7b2e6a16
Revises: 28f62b6e1f24
Create Date: 2016-03-01 11:46:58.147000

"""

# revision identifiers, used by Alembic.
revision = 'ee6b7b2e6a16'
down_revision = '28f62b6e1f24'

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import ENUM

# enum type
user_status_enum = sa.Enum('new', 'confirmed', 'deleted', name="status_enum")

def upgrade():
	# create new type
    user_status_enum.create(op.get_bind())

    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('status', user_status_enum, nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    ### end Alembic commands ###

	# drop type
    user_status_enum.drop(op.get_bind())