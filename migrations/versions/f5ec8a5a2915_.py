"""empty message

Revision ID: f5ec8a5a2915
Revises: a4d0e7345570
Create Date: 2023-12-05 11:02:41.006231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5ec8a5a2915'
down_revision = 'a4d0e7345570'
branch_labels = None
depends_on = None

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=(SCHEMA if environment == 'production' else None)) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=75), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=(SCHEMA if environment == 'production' else None)) as batch_op:
        batch_op.drop_column('profile_picture')

    # ### end Alembic commands ###
