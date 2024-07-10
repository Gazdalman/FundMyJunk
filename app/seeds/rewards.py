from app.models import db, Reward, environment, SCHEMA
from sqlalchemy.sql import text
from faker import Faker
from random import choice, randint

fake = Faker()
adjectives = [
    "adorable", "adventurous", "agreeable", "alert", "ambitious",
    "amused", "arrogant", "awkward", "bad", "beautiful",
    "brave", "bright", "careless", "charming", "cheerful",
    "clumsy", "cooperative", "courageous", "cruel", "curious",
    "delightful", "determined", "dull", "eager", "easygoing",
    "efficient", "energetic", "enthusiastic", "exuberant", "faithful",
    "fantastic", "fearless", "foolish", "friendly", "funny",
    "generous", "gentle", "glorious", "good", "grumpy",
    "happy", "helpful", "hilarious", "hopeful", "hostile",
    "innovative", "intelligent", "jolly", "joyful", "kind",
    "lazy", "lively", "lovely", "lucky", "mean",
    "mysterious", "nasty", "naughty", "nice", "obnoxious",
    "optimistic", "passionate", "patient", "peaceful", "perfect",
    "polite", "proud", "relaxed", "reliable", "romantic",
    "rude", "silly", "sincere", "smart", "splendid",
    "stubborn", "successful", "superb", "supportive", "talented",
    "thankful", "thoughtful", "thrifty", "unfriendly", "unlucky",
    "victorious", "vivacious", "witty", "wonderful", "worthless",
    "zealous", "zestful", "zesty", "adorable", "brilliant",
    "creative", "dedicated", "diligent", "elegant", "eloquent",
    "graceful", "harmonious", "honest", "innocent", "insightful",
    "interesting", "majestic", "mysterious", "noble", "persistent",
    "suspicious", "vibrant"
]

# Adds a demo reward, you can add other rewards here if you want
def seed_rewards():
  for id in range(1,51):
    reward1 = Reward(
      project_id=id,
      image="https://picsum.photos/850/400",
      title=f"A Very {fake.word(ext_word_list=adjectives).title()} Something or Other",
      description=fake.sentence(),
      physical_items=True,
      shipping=choice(["Digital rewards", "Local event", "Ships to anywhere"]),
      delivery_date=fake.future_date(end_date='+100d'),
      amount=randint(1,80000),
      unlimited=True
    )
    reward2 = Reward(
      project_id=id,
      image="https://picsum.photos/850/400",
      title=f"A Very {fake.word(ext_word_list=adjectives).title()} Something or Other",
      description=fake.sentence(),
      physical_items=True,
      shipping=choice(["Digital rewards", "Local event", "Ships to anywhere"]),
      delivery_date=fake.future_date(end_date='+100d'),
      amount=randint(1,80000),
      unlimited=False,
      quantity=randint(1,100)
    )
    reward3 = Reward(
      project_id=id,
      image="https://picsum.photos/850/400",
      title=f"A Very {fake.word(ext_word_list=adjectives).title()} Something or Other",
      description=fake.sentence(),
      physical_items=True,
      shipping=choice(["Digital rewards", "Local event", "Ships to anywhere"]),
      delivery_date=fake.future_date(end_date='+100d'),
      amount=randint(1,80000),
      unlimited=True
    )

    db.session.add(reward1)
    db.session.add(reward2)
    db.session.add(reward3)
  db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the rewards table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.

def does_table_exist(table_name, schema_name):
    query = text(
        f"""
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

def undo_rewards():
    if environment == "production":
      if does_table_exist("rewards", SCHEMA):
        db.session.execute(f"TRUNCATE table {SCHEMA}.rewards RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM rewards"))

    db.session.commit()
