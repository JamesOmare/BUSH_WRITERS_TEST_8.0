"""empty message

Revision ID: 76075f0b1841
Revises: a14d44b41647
Create Date: 2022-12-18 05:04:25.615849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76075f0b1841'
down_revision = 'a14d44b41647'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('confirmation', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_confirmation_confirmation_msg'), ['confirmation_msg'])

    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.add_column(sa.Column('account_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_notification_account_id_account'), 'account', ['account_id'], ['account_id'], ondelete='CASCADE')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_user_phone_number'), ['phone_number'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_phone_number'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_user_email'), type_='unique')

    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_notification_account_id_account'), type_='foreignkey')
        batch_op.drop_column('account_id')

    with op.batch_alter_table('confirmation', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_confirmation_confirmation_msg'), type_='unique')

    # ### end Alembic commands ###