"""Add author field to Content

Revision ID: 09c9c21d7b43
Revises: d2754bdbafaf
Create Date: 2024-09-20 14:18:03.816881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c9c21d7b43'
down_revision = 'd2754bdbafaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('content', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.String(length=150), nullable=False))
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               type_=sa.String(length=500),
               existing_nullable=False)
        batch_op.alter_column('link',
               existing_type=sa.VARCHAR(length=300),
               type_=sa.String(length=500),
               existing_nullable=True)
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('content', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), nullable=True))
        batch_op.alter_column('link',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=300),
               existing_nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.String(length=500),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.drop_column('author')

    # ### end Alembic commands ###
