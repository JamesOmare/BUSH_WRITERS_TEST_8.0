"""empty message

Revision ID: 161e0776595d
Revises: 0ebfd48b3deb
Create Date: 2023-01-04 12:18:20.373399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '161e0776595d'
down_revision = '0ebfd48b3deb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account_credentials', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_account_credentials_account_id_account'), 'account', ['account_id'], ['account_id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account_credentials', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_account_credentials_account_id_account'), type_='foreignkey')

    # ### end Alembic commands ###
