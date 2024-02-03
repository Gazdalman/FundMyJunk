from app.models import db, Project, environment, SCHEMA, Backer, Project
from faker import Faker
from random import randint, choice
from sqlalchemy.sql import text


fake = Faker()

def seed_pledges():

  projects = Project.query.all()

  proj_dict = {project.id: project for project in projects}

  for _ in range(200):
    id = randint(1,10)
    proj_id = randint(1,50)

    pledge = Backer(
      project_id=proj_id,
      user_id=id if proj_dict[proj_id].user_id != id else None,
      amount=randint(1,100000)
    )

    db.session.add(pledge)

    for reward in proj_dict[proj_id].rewards:
            if reward.amount <= pledge.amount and (reward.unlimited or reward.quantity > 0):
                pledge.rewards.append(reward)
                if not reward.unlimited:
                    reward.quantity = reward.quantity - 1

    proj_dict[proj_id].earned_today = proj_dict[proj_id].earned_today + pledge.amount
  db.session.commit()

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

def undo_pledges():
    if environment == "production":
        if does_table_exist("backers", SCHEMA):
            db.session.execute(f"TRUNCATE table {SCHEMA}.backers RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM backers"))

    db.session.commit()
