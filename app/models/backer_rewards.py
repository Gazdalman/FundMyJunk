from .db import db, environment, SCHEMA, add_prefix_for_prod

class BackerReward(db.Model):
  __tablename__ = "backer_rewards"

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.Integer, primary_key=True)
  backer_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("backers.id")), nullable=False)
  reward_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("rewards.id")), nullable=False)

