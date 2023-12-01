from .db import db, environment, SCHEMA, add_prefix_for_prod

class RewardItem(db.Model):
  __tablename__ = "reward_items"

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.INTEGER, primary_key=True)
  reward_id = db.Column(db.INTEGER, db.ForeignKey(add_prefix_for_prod("rewards.id")), nullable=False)
  title = db.Column(db.String(50), nullable=False)
  quantity = db.Column(db.INTEGER, nullable=False)
  image = db.Column(db.String(50))

  reward = db.relationship(
    "Reward",
    back_populates="items"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "image": self.image,
      "quantity": self.quantity
    }
