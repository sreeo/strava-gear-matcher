"""Init migration

Revision ID: 1b2b0e3a5fc0
Create Date: 2024-07-03 11:51:02.626647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b2b0e3a5fc0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('strava_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=512), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('strava_id')
                    )
    op.create_table('gear',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('strava_gear_id', sa.String(
                        length=120), nullable=False),
                    sa.Column('name', sa.String(length=512), nullable=False),
                    sa.Column('type', sa.String(length=128), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(
                        length=512), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('strava_gear_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gear')
    op.drop_table('user')
    # ### end Alembic commands ###