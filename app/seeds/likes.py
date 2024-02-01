from app.models import db, Project, environment, SCHEMA
from faker import Faker
from random import randint, choice
from sqlalchemy.sql import text

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

def undo_likes():
    if environment == "production":
        if does_table_exist("likes", SCHEMA):
            db.session.execute(f"TRUNCATE table {SCHEMA}.likes RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM likes"))

    db.session.commit()
