"""empty message

Revision ID: 587c36f58532
Revises: b76ce31794ae
Create Date: 2022-12-14 23:23:54.575094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '587c36f58532'
down_revision = 'b76ce31794ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('confirmation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('if_rejected', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('if_accepted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('confirmation', schema=None) as batch_op:
        batch_op.drop_column('if_accepted')
        batch_op.drop_column('if_rejected')

    # ### end Alembic commands ###
