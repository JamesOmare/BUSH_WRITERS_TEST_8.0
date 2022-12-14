"""empty message

Revision ID: d5fef6c88051
Revises: 0d5494a80fba
Create Date: 2022-12-18 04:54:53.385784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5fef6c88051'
down_revision = '0d5494a80fba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.add_column(sa.Column('account_owner_id', sa.String(length=10), nullable=True))
        batch_op.create_foreign_key(None, 'account', ['account_id'], ['account_id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('account_owner_id')

    # ### end Alembic commands ###
