"""empty message

Revision ID: eadd3626a67f
Revises: d3056fbec50a
Create Date: 2020-05-02 14:41:40.959133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eadd3626a67f'
down_revision = 'd3056fbec50a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('num_upcoming_shows', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'num_upcoming_shows')
    # ### end Alembic commands ###
