"""empty message

Revision ID: 85d398d12ae2
Revises: 1cc22f34933d
Create Date: 2022-11-27 11:07:15.555737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d398d12ae2'
down_revision = '1cc22f34933d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_number', sa.String(length=15), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.drop_column('payment_number')

    # ### end Alembic commands ###
