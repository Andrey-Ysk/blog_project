"""empty message

Revision ID: fb2ab322e6de
Revises: 304fbd6a7e5f
Create Date: 2021-03-25 02:58:13.742321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb2ab322e6de'
down_revision = '304fbd6a7e5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts_rating', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_vote', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts_rating', schema=None) as batch_op:
        batch_op.drop_column('last_vote')

    # ### end Alembic commands ###
