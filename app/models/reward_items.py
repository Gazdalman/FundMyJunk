from .db import db, environment, SCHEMA, add_prefix_for_prod
from .aws_helper import remove_file_from_s3
from sqlalchemy import event

class RewardItem(db.Model):
  __tablename__ = "reward_items"

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.Integer, primary_key=True)
  reward_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("rewards.id")), nullable=False)
  title = db.Column(db.String(150), nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  image = db.Column(db.String(150))

  reward = db.relationship(
    "Reward",
    back_populates="items"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "rewardId": self.reward_id,
      "title": self.title,
      "image": self.image,
      "quantity": self.quantity
    }

def on_item_delete(mapper, connection, target):
  if target.image:
    remove_file_from_s3(target.image)
  return 'blah'

event.listen(RewardItem, 'before_delete', on_item_delete)
