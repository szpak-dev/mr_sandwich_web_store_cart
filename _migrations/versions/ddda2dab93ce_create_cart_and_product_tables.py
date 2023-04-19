"""create cart and product tables

Revision ID: ddda2dab93ce
Revises: 
Create Date: 2023-01-06 03:31:26.025628

"""
from alembic import op
import sqlalchemy as sa


revision = 'ddda2dab93ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('carts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('customer_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('total_price', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_table('cart_products',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('cart_id', sa.Integer(), sa.ForeignKey('carts.id'), nullable=True),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('product_name', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('cart_products')
    op.drop_table('carts')
