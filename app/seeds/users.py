from app.models import db, User, environment, SCHEMA, UserProfile
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

    profile = UserProfile(
        user_id=user.id,
        bio='I am a demo user',
        first_name='Demo',
        last_name='Noodle',
        location= f"{fake.city()}, {fake.state()}",
        website='https://gazdalman.github.io/',
        private=False,
    )

    user.profile.append(profile)

    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password='password',
            display_name=fake.name(),
        )

        db.session.add(user)

        profile = UserProfile(
            bio=fake.text(max_nb_chars=500),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            location= f"{fake.city()}, {fake.state()}",
            website="https://gazdalman.github.io/",
            private=choice([True, False]),
        )

        user.profile.append(profile)


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
        if does_table_exist("user_profiles", SCHEMA):
            db.session.execute(f"TRUNCATE table {SCHEMA}.user_profiles RESTART IDENTITY CASCADE;")

        if does_table_exist("users", SCHEMA):
            db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM user_profiles"))
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
