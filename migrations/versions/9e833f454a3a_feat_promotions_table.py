"""feat: promotions table

Revision ID: 9e833f454a3a
Revises: f4f7c1e026a5
Create Date: 2025-05-02 19:16:53.779571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e833f454a3a'
down_revision = 'f4f7c1e026a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promotions',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('promo_code', sa.String(length=20), nullable=False),
    sa.Column('discount_value', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('promotion_type', sa.Enum('PERCENTAGE_DISCOUNT', 'FIXED_DISCOUNT', 'FREE_SHIPPING', 'BUY_X_GET_Y', name='promotiontype'), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('min_order_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('max_discount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('usage_limit', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('promo_code')
    )
    op.create_table('promotion_product_association',
    sa.Column('promotion_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['promotion_id'], ['promotions.id'], ),
    sa.PrimaryKeyConstraint('promotion_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('promotion_product_association')
    op.drop_table('promotions')
    # ### end Alembic commands ###
