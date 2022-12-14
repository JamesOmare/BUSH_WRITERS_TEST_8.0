"""empty message

Revision ID: 655ed8864358
Revises: 4e5a0e58b2ba
Create Date: 2022-09-26 21:18:55.435520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '655ed8864358'
down_revision = '4e5a0e58b2ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('admin')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
