from app.models import db, Story, environment, SCHEMA
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

# Adds a demo story, you can add other stories here if you want
def seed_stories():
  for id in range(1,51):
    story = Story(
      project_id=id,
      ai=choice([True,False]),
      story_text=fake.paragraph(nb_sentences=3),
      risks_challenges=fake.paragraph(nb_sentences=5)
    )

    db.session.add(story)
  db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the stories table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_stories():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.stories RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM stories"))

    db.session.commit()
