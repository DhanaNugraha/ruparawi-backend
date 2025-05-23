"""feat: removed vendor review

Revision ID: c19fe7f65b50
Revises: ca8dd253a184
Create Date: 2025-05-03 10:30:43.993122

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c19fe7f65b50'
down_revision = 'ca8dd253a184'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vendor_testimonials',
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin_users.user_id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendor_profiles.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('vendor_reviews')
    with op.batch_alter_table('product_reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.Text(), nullable=True))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('review_text')
        batch_op.drop_column('is_approved')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_approved', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('review_text', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('comment')

    op.create_table('vendor_reviews',
    sa.Column('vendor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('review_text', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='vendor_reviews_user_id_fkey'),
    sa.ForeignKeyConstraint(['vendor_id'], ['users.id'], name='vendor_reviews_vendor_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='vendor_reviews_pkey')
    )
    op.drop_table('vendor_testimonials')
    # ### end Alembic commands ###
