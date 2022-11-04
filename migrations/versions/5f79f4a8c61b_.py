"""empty message

Revision ID: 5f79f4a8c61b
Revises: e912adb151ca
Create Date: 2022-11-03 15:34:48.083071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f79f4a8c61b'
down_revision = 'e912adb151ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_credentials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('account_name', sa.String(length=150), nullable=True),
    sa.Column('account_type', sa.String(length=50), nullable=True),
    sa.Column('account_email', sa.String(length=100), nullable=True),
    sa.Column('account_url', sa.String(length=250), nullable=True),
    sa.Column('account_passphrase', sa.String(length=250), nullable=True),
    sa.Column('time_posted', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account_credentials')
    # ### end Alembic commands ###