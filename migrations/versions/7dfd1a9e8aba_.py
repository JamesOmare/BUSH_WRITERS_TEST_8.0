"""empty message

Revision ID: 7dfd1a9e8aba
Revises: 3bab028c3278
Create Date: 2022-11-05 06:41:32.081716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dfd1a9e8aba'
down_revision = '3bab028c3278'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account_credentials', schema=None) as batch_op:
        batch_op.add_column(sa.Column('buyer_id', sa.Integer(), nullable=True))

    with op.batch_alter_table('complaint', schema=None) as batch_op:
        batch_op.add_column(sa.Column('buyer_id', sa.Integer(), nullable=True))
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complaint', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        batch_op.drop_column('buyer_id')

    with op.batch_alter_table('account_credentials', schema=None) as batch_op:
        batch_op.drop_column('buyer_id')

    # ### end Alembic commands ###
