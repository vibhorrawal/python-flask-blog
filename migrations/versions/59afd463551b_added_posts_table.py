"""Added Posts table

Revision ID: 59afd463551b
Revises: 79fe69aa8d0e
Create Date: 2018-10-15 21:03:03.041221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59afd463551b'
down_revision = '79fe69aa8d0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_body'), 'post', ['body'], unique=False)
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_index(op.f('ix_post_body'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###
