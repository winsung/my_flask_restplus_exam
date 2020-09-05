"""create

Revision ID: 3bfb412d1b75
Revises: 
Create Date: 2020-09-06 00:41:13.495567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bfb412d1b75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.String(20), primary_key=True),
        sa.Column('password', sa.String(80), nullable=False),
        sa.Column('last_logout_dt', sa.DateTime),
        sa.Column('signout_dt', sa.DateTime),
        sa.Column('create_dt', sa.DateTime)
    )
    op.create_table(
        'session',
        sa.Column('session_id', sa.String(20), primary_key=True),
        sa.Column('logout_dt', sa.DateTime),
        sa.Column('id', sa.String(20)),
        sa.Column('client_ip', sa.String(15)),
        sa.Column('create_dt', sa.DateTime)
    )


def downgrade():
    op.drop_table('user')
    op.drop_table('session')
