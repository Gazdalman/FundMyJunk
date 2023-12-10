from .db import db, environment, SCHEMA, add_prefix_for_prod

class Backer(db.Model):
  __tablename__ = 'backers'

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("projects.id")), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
  amount = db.Column(db.FLOAT, nullable=False)

  project = db.relationship(
    "Project",
    back_populates="backers"
  )
