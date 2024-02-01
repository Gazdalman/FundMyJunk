"""empty message

Revision ID: 809c4ffabb0a
Revises: 2afb0181d08f
Create Date: 2024-01-30 10:39:18.855482

"""
from alembic import op
import sqlalchemy as sa

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

# revision identifiers, used by Alembic.
revision = '809c4ffabb0a'
down_revision = '2afb0181d08f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('backers', schema=(SCHEMA if environment == "production" else None)) as batch_op:
        batch_op.alter_column('project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('backers', schema=(SCHEMA if environment == "production" else None)) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('project_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###