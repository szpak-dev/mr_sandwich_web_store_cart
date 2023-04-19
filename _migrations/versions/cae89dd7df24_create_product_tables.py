"""create product tables

Revision ID: cae89dd7df24
Revises: ddda2dab93ce
Create Date: 2023-01-06 18:00:32.609218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cae89dd7df24'
down_revision = 'ddda2dab93ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('calories_per_100g', sa.Float(), nullable=True),
        sa.Column('calories_per_serving', sa.Float(), nullable=True),
        sa.Column('ingredients', sa.Text(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('products')
