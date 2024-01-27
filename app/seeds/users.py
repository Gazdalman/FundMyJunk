from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text
from faker import Faker
from random import choice
fake = Faker()


# Adds a demo user, you can add other users here if you want
def seed_users():
    user = User(
        username='demoNoodle',
        email='demo@aa.io',
        password='password',
        display_name='Demoted INC',
    )
    db.session.add(user)

    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password='password',
            display_name=fake.name(),
        )

        db.session.add(user)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.

def does_table_exist(table_name, schema_name):
    query = text(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = :schema AND table_name = :table
        );
        """
    )

    result = db.session.execute(query, {'schema': schema_name, 'table': table_name})
    exists = result.scalar()
    return exists

def undo_users():
    if environment == "production":
        if does_table_exist("users", SCHEMA):
            db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
