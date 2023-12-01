"""empty message

Revision ID: a5ad9c34e1b2
Revises:
Create Date: 2023-11-30 18:50:28.522418

"""
from alembic import op
import sqlalchemy as sa

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

# revision identifiers, used by Alembic.
revision = 'a5ad9c34e1b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('user_credit', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )

    if environment == "production":
        op.execute(f"ALTER TABLE users SET SCHEMA {SCHEMA};")

    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=60), nullable=False),
    sa.Column('subtitle', sa.String(length=135), nullable=False),
    sa.Column('location', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(length=150), nullable=False),
    sa.Column('video', sa.String(length=150), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('goal', sa.FLOAT(), nullable=False),
    sa.Column('main_category', sa.String(length=50), nullable=False),
    sa.Column('main_subcat', sa.String(length=50), nullable=False),
    sa.Column('second_cat', sa.String(length=50), nullable=True),
    sa.Column('second_subcat', sa.String(length=50), nullable=True),
    sa.Column('launch_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    if environment == "production":
        op.execute(f"ALTER TABLE projects SET SCHEMA {SCHEMA};")

    op.create_table('rewards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(length=50), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=True),
    sa.Column('physical_items', sa.Boolean(), nullable=False),
    sa.Column('shipping', sa.String(length=50), nullable=False),
    sa.Column('delivery_date', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.FLOAT(), nullable=False),
    sa.Column('unlimited', sa.Boolean(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    if environment == "production":
        op.execute(f"ALTER TABLE rewards SET SCHEMA {SCHEMA};")

    op.create_table('stories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('ai', sa.Boolean(), nullable=False),
    sa.Column('story_text', sa.String(length=2000), nullable=False),
    sa.Column('risks_challenges', sa.String(length=2500), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    if environment == "production":
        op.execute(f"ALTER TABLE stories SET SCHEMA {SCHEMA};")

    op.create_table('reward_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reward_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['reward_id'], ['rewards.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    if environment == "production":
        op.execute(f"ALTER TABLE reward_items SET SCHEMA {SCHEMA};")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reward_items')
    op.drop_table('stories')
    op.drop_table('rewards')
    op.drop_table('projects')
    op.drop_table('users')
    # ### end Alembic commands ###
