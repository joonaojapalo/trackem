"""empty message

Revision ID: ce79c48e8188
Revises: 2f8bcb8b3319
Create Date: 2016-03-04 13:32:19.602000

"""

# revision identifiers, used by Alembic.
revision = 'ce79c48e8188'
down_revision = '2f8bcb8b3319'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_group', sa.Column('issued', sa.Float(), nullable=True))
    op.drop_column('user_group', 'added')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_group', sa.Column('added', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('user_group', 'issued')
    ### end Alembic commands ###