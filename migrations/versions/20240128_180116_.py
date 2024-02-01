"""empty message

Revision ID: 41776f22757b
Revises: 646c1a32c1a1
Create Date: 2024-01-28 18:01:16.077512

"""
from alembic import op
import sqlalchemy as sa

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

# revision identifiers, used by Alembic.
revision = '41776f22757b'
down_revision = '646c1a32c1a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=(SCHEMA if environment == "production" else None)) as batch_op:
        batch_op.add_column(sa.Column('earned_today', sa.FLOAT()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=(SCHEMA if environment == "production" else None)) as batch_op:
        batch_op.drop_column('earned_today')

    # ### end Alembic commands ###
