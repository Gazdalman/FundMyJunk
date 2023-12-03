from app.models import db, Project, environment, SCHEMA
from sqlalchemy.sql import text
from faker import Faker
from random import choice, randint
from datetime import datetime, timedelta

categories = ["Art", "Comics","Crafts","Dance","Design","Fashion","Film & Video","Food","Games","Journalism","Music","Photography","Publishing","Technology","Theater"]
fake = Faker()
num = 1
adjectives = [
    "adorable", "agreeable", "ambitious", "brave", "calm", "charming",
    "cheerful", "considerate", "cooperative", "courageous", "delightful",
    "determined", "eager", "easygoing", "efficient", "energetic", "enthusiastic",
    "exuberant", "faithful", "fantastic", "fearless", "friendly", "funny",
    "generous", "gentle", "grateful", "handsome", "happy", "helpful",
    "hilarious", "honest", "hopeful", "humble", "innovative", "intelligent",
    "jolly", "joyful", "kind", "lovely", "lucky", "modest",
    "optimistic", "peaceful", "polite", "proud", "relaxed", "reliable",
    "sincere", "thoughtful", "trustworthy", "vivacious", "witty"
]

# Adds a demo project, you can add other projects here if you want
def seed_projects():
  for _ in range(50):
    launch = datetime.now()
    end = launch + timedelta(days=randint(1,60))
    project = Project(
      user_id=choice(range(1, 11)),
      title=f"The {fake.word(ext_word_list=adjectives).title()} Project",
      subtitle="Nothing to see here folks, just give me money",
      location='nowhere, Alaska',
      main_category=choice(categories),
      main_subcat="banana",
      image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFFFdyEuFvw9ktw7vI0Q5l1JFHKmXVI_8W5mNhLPxhnJKhe8Wf08hr1BAXBaS3nGpBqaI&usqp=CAU",
      type=choice(['individual', 'business', 'non-profit']),
      goal=randint(1, 1000000),
      launch_date=launch,
      end_date=end,
      launched=choice([True,False])
    )
    db.session.add(project)
  db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the projects table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_projects():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.projects RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM projects"))

    db.session.commit()
