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
        first_name='Demo',
        last_name='Noodle',
        password='password',
        display_name='Demoted INC',
        private=False,
        biography="This is the demo user created for you to experiment with. Now go frivolously spend money!"
    )
    db.session.add(user)

    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password='password',
            display_name=fake.name(),
            private=choice([True,False]),
            biography=fake.paragraph()
        )

        db.session.add(user)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
