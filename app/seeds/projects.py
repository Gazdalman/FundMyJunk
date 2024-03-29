from app.models import db, Project, environment, SCHEMA
from sqlalchemy.sql import text
from faker import Faker
from random import choice, randint
from datetime import datetime, timedelta
import requests

categories = ["Art", "Comics","Crafts","Dance","Design","Eldritch Horror","Fashion","Film & Video","Food","Games","Journalism","Music","Photography","Publishing","Technology","Theater"]
fake = Faker()
subcategories = {
  "Art": [
    "Ceramics",
    "Conceptual Art",
    "Digital Art",
    "Illustration",
    "Installations",
    "Mixed Media",
    "Painting",
    "Performance Art",
    "Public Art",
    "Sculpture",
    "Social Practice",
    "Textiles",
    "Video Art"
  ],
  "Comics": [
    "Anthologies",
    "Comic Books",
    "Events",
    "Graphic Novels",
    "Web Comics"
  ],
  "Crafts": [
    "Candles",
    "Crochet",
    "DIY",
    "Embroidery",
    "Glass",
    "Knitting",
    "Pottery",
    "Printing",
    "Quilts",
    "Stationery",
    "Taxidermy",
    "Weaving",
    "Woodworking"
  ],
  "Dance": [
    "Performances",
    "Residences",
    "Spaces",
    "Workshops"
  ],
  "Design": [
    "Architecture",
    "Civic Design",
    "Graphic Design",
    "Interactive Design",
    "Product Design",
    "Toys",
    "Typography"
  ],
  "Eldritch Horror": [
    "Ancient Texts",
    "Live Entities",
    "Observation",
    "Research"
  ],
  "Fashion": [
    "Accessories",
    "Apparel",
    "Children's Wear",
    "Couture",
    "Footwear",
    "Jewelry",
    "Pet Fashion",
    "Ready-to-Wear"
  ],
  "Film & Video": [
    "Action",
    "Animation",
    "Comedy",
    "Documentary",
    "Drama",
    "Experimental",
    "Family",
    "Fantasy",
    "Festivals",
    "Horror",
    "Movie Theaters",
    "Music Videos",
    "Narrative Film",
    "Romance",
    "Science Fiction",
    "Shorts",
    "Television"
  ],
  "Food": [
    "Butchery",
    "Community Gardens",
    "Cookbooks",
    "Drinks",
    "Events",
    "Farmer's Market",
    "Farms",
    "Food Trucks",
    "Restaurants",
    "Small Batch",
    "Spaces",
    "Vegan"
  ],
  "Games": [
    "Gaming Hardware",
    "Live Games",
    "Mobile Games",
    "Playing Cards",
    "Puzzles",
    "Tabletop Gaming",
    "Video Games"
  ],
  "Journalism": [
    "Audio",
    "Photo",
    "Print",
    "Video",
    "Web"
  ],
  "Music": [
    "Blues",
    "Chiptune",
    "Classical Music",
    "Comedy",
    "Country & Folk",
    "Electronic Music",
    "Faith",
    "Hip-Hop",
    "Indie Rock",
    "Jazz",
    "Kids",
    "Latin",
    "Metal",
    "Pop",
    "Punk",
    "R&B",
    "Rock",
    "Studios",
    "World Music"
  ],
  "Photography": [
    "Animals",
    "Fine Art",
    "Nature",
    "People",
    "Photo Albums",
    "Places"
  ],
  "Publishing": [
    "Academic",
    "Anthologies",
    "Art Books",
    "Calendars",
    "Children's Books",
    "Comedy",
    "Fiction",
    "Letterpress",
    "Literary Journals",
    "Literary Spaces",
    "Nonfiction",
    "Periodicals",
    "Poetry",
    "Radio & Podcasts",
    "Translate",
    "Young Adult",
    "Zines"
  ],
  "Technology": [
    "3D Printing",
    "Apps",
    "Artificial Intelligence",
    "Camera Equipment",
    "DIY Electronics",
    "Fabrication Tools",
    "Flight",
    "Gadgets",
    "Hardware",
    "Marketplaces",
    "Robots",
    "Software",
    "Sound",
    "Space Exploration",
    "Wearables",
    "Web"
  ],
  "Theater": [
    "Comedy",
    "Experimental",
    "Festivals",
    "Immersive",
    "Musical",
    "Plays",
    "Spaces"
  ]
}
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

    res = requests.get("https://picsum.photos/850/400")

    if res.status_code == 200:
      img_url = res.url
    else:
      img_url = "https://picsum.photos/450/500"

    launch = datetime.now()
    end = launch + timedelta(days=randint(1,60))
    cat = choice(categories)

    project = Project(
      user_id=choice(range(1, 11)),
      title=f"The {fake.word(ext_word_list=adjectives).title()} Project",
      subtitle="Nothing to see here folks, just give me money",
      location='nowhere, Alaska',
      main_category=cat,
      main_subcat=choice(subcategories[cat]),
      image=img_url,
      type=choice(['individual', 'business', 'non-profit']),
      goal=randint(1, 1000000),
      launch_date=launch,
      end_date=end,
      launched=choice([True,False])
    )

    if (project.launch_date <= datetime.now()):
      project.launched = True
    else:
      project.launched = False

    db.session.add(project)
  db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the projects table. SQLAlchemy doesn't
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

def undo_projects():
    if environment == "production":
        if does_table_exist("projects", SCHEMA):
          db.session.execute(f"TRUNCATE table {SCHEMA}.projects RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM projects"))

    db.session.commit()
