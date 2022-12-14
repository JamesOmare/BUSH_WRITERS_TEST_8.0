"""empty message

Revision ID: c35cec0bc048
Revises: 85d398d12ae2
Create Date: 2022-11-27 11:09:18.870144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c35cec0bc048'
down_revision = '85d398d12ae2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mpesa_fee', sa.Integer(), nullable=True))
        batch_op.drop_column('safaricom_fee')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('safaricom_fee', sa.INTEGER(), nullable=True))
        batch_op.drop_column('mpesa_fee')

    # ### end Alembic commands ###
