"""empty message

Revision ID: 3034e6db891d
Revises: cddcf150e0a0
Create Date: 2022-12-17 21:47:09.089151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3034e6db891d'
down_revision = 'cddcf150e0a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.VARCHAR(length=10), nullable=True))

    # ### end Alembic commands ###