"""empty message

Revision ID: 2c5fc0f9ad45
Revises: bcf94c41e9a
Create Date: 2015-10-26 17:41:27.453000

"""

# revision identifiers, used by Alembic.
revision = '2c5fc0f9ad45'
down_revision = 'bcf94c41e9a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('memberbucketstore',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('bucket', sa.String(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('access_key_selector', sa.String(length=30), nullable=True),
    sa.Column('access_key_id', sa.String(), nullable=False),
    sa.Column('secret_access_key', sa.String(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('apscheduler_jobs')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apscheduler_jobs',
    sa.Column('id', sa.VARCHAR(length=191), autoincrement=False, nullable=False),
    sa.Column('next_run_time', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('job_state', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.Column('member_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'apscheduler_jobs_pkey')
    )
    op.drop_table('memberbucketstore')
    ### end Alembic commands ###
