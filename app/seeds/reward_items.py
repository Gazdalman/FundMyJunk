from app.models import db, RewardItem, environment, SCHEMA
from sqlalchemy.sql import text
from random import randint, choice

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

# Adds a demo reward_item, you can add other reward_items here if you want
def seed_reward_items():
  for id in range(1,151):
    reward_item1 = RewardItem(
      reward_id=id,
      image="https://m.media-amazon.com/images/M/MV5BMTczNDc4OTU5NF5BMl5BanBnXkFtZTcwMjY1NzkyMw@@._V1_.jpg",
      title=f"A Very {choice(adjectives).title()} Something",
      quantity=randint(1,5)
    )
    reward_item2 = RewardItem(
      reward_id=id,
      image="https://m.media-amazon.com/images/M/MV5BMTczNDc4OTU5NF5BMl5BanBnXkFtZTcwMjY1NzkyMw@@._V1_.jpg",
      title=f"A Very {choice(adjectives).title()} Something",
      quantity=randint(1,5)
    )
    reward_item3 = RewardItem(
      reward_id=id,
      image="https://m.media-amazon.com/images/M/MV5BMTczNDc4OTU5NF5BMl5BanBnXkFtZTcwMjY1NzkyMw@@._V1_.jpg",
      title=f"A Very {choice(adjectives).title()} Something",
      quantity=randint(1,5)
    )

    db.session.add(reward_item1)
    db.session.add(reward_item2)
    db.session.add(reward_item3)
  db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the reward_items table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_reward_items():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.reward_items RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reward_items"))

    db.session.commit()
