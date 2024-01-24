from .db import db, environment, SCHEMA, add_prefix_for_prod
from .aws_helper import remove_file_from_s3
from sqlalchemy import event
from datetime import datetime
from .likes import Like

class Project(db.Model):
  __tablename__ = "projects"

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
  title = db.Column(db.String(60), nullable=False)
  subtitle = db.Column(db.String(135), nullable=False)
  location = db.Column(db.String(50), nullable=False)
  image = db.Column(db.String(150), nullable=False)
  video = db.Column(db.String(150))
  type = db.Column(db.String(50), nullable=False)
  goal = db.Column(db.FLOAT, nullable=False)
  main_category = db.Column(db.String(50), nullable=False)
  main_subcat = db.Column(db.String(50), nullable=False)
  second_cat = db.Column(db.String(50))
  second_subcat = db.Column(db.String(50))
  launch_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)
  launched = db.Column(db.Boolean, nullable=False, default=False)

  user = db.relationship(
    "User",
    back_populates="projects"
  )

  story = db.relationship(
    "Story",
    back_populates="project",
    cascade="all, delete-orphan"
  )

  rewards = db.relationship(
    "Reward",
    back_populates="project",
    cascade="all, delete-orphan"
  )

  liked_users = db.relationship(
    "User",
    secondary=Like.__table__,
    back_populates="liked_projects"
  )

  backers = db.relationship(
    "Backer",
    back_populates="project"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "userId": self.user_id,
      "title": self.title,
      "subtitle": self.subtitle,
      "location": self.location,
      "type": self.type,
      "image": self.image,
      "video": self.video,
      "goal": self.goal,
      "launchDate": self.launch_date,
      "endDate": self.end_date,
      "story": [story.to_dict() for story in self.story][0] if self.story else "",
      "mainCategory": self.main_category,
      "mainSub": self.main_subcat,
      "secondCat": self.second_cat if self.second_cat else '',
      "secondSub": self.second_subcat if self.second_subcat else '',
      "rewards": sorted([reward.to_dict() for reward in self.rewards], key=lambda reward : reward['amount']),
      "launched": self.launch_date <= datetime.now(),
      "user": self.user.display_name,
      "earned": sum([backer.amount for backer in self.backers])
    }

def on_project_delete(mapper, connection, target):
  remove_file_from_s3(target.image)
  if target.video:
    remove_file_from_s3(target.video)
  return 'blah'

event.listen(Project, 'before_delete', on_project_delete)
