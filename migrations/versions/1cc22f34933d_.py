"""empty message

Revision ID: 1cc22f34933d
Revises: 1f3ed549a976
Create Date: 2022-11-25 14:36:28.420476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cc22f34933d'
down_revision = '1f3ed549a976'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('payment_method', sa.String(length=50), nullable=False),
    sa.Column('transaction_id', sa.String(length=50), nullable=False),
    sa.Column('country_code', sa.String(length=50), nullable=False),
    sa.Column('gross_pay', sa.Integer(), nullable=False),
    sa.Column('paypal_fee', sa.Integer(), nullable=True),
    sa.Column('paypal_email', sa.String(length=250), nullable=True),
    sa.Column('safaricom_fee', sa.Integer(), nullable=True),
    sa.Column('net_pay', sa.Integer(), nullable=True),
    sa.Column('currency_paid', sa.String(length=80), nullable=False),
    sa.Column('transaction_date', sa.String(length=50), nullable=False),
    sa.Column('transaction_time', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    # ### end Alembic commands ###
