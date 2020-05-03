"""empty message

Revision ID: 83f3bba3e2bc
Revises: 271270fbda58
Create Date: 2020-05-03 09:13:43.628719

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '83f3bba3e2bc'
down_revision = '271270fbda58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('num_past_shows', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('num_upcoming_shows', sa.Integer(), nullable=True))
    op.alter_column('Show', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Show', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('Artist', 'num_upcoming_shows')
    op.drop_column('Artist', 'num_past_shows')
    # ### end Alembic commands ###
