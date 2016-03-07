"""empty message

Revision ID: 61ce3cd8bf5d
Revises: baf14df5c20b
Create Date: 2016-03-07 13:26:34.245000

"""

# revision identifiers, used by Alembic.
revision = '61ce3cd8bf5d'
down_revision = 'baf14df5c20b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('map', sa.Column('group', sa.Integer(), nullable=False))
    op.drop_constraint(u'map_map_fkey', 'map', type_='foreignkey')
    op.create_foreign_key(None, 'map', 'group', ['group'], ['id'])
    op.drop_column('map', 'map')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('map', sa.Column('map', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'map', type_='foreignkey')
    op.create_foreign_key(u'map_map_fkey', 'map', 'map', ['map'], ['id'])
    op.drop_column('map', 'group')
    ### end Alembic commands ###
