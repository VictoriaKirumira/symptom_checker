"""Initial migration

Revision ID: 0200e579d4b2
Revises: 
Create Date: 2024-10-20 14:16:38.168589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0200e579d4b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('symptom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symptom_list', sa.String(length=500), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('symptom')
    op.drop_table('user')
    # ### end Alembic commands ###
