from .db import db, environment, SCHEMA, add_prefix_for_prod
from .aws_helper import remove_file_from_s3
from sqlalchemy import event

class Reward(db.Model):
  __tablename__ = "rewards"

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("projects.id")), nullable=False)
  image = db.Column(db.String(1000), nullable=False)
  title = db.Column(db.String(50), nullable=False)
  description = db.Column(db.String(2000))
  physical_items = db.Column(db.Boolean, nullable=False, default=False)
  shipping = db.Column(db.String(50), nullable=False)
  delivery_date = db.Column(db.DateTime, nullable=False)
  amount = db.Column(db.FLOAT, nullable=False)
  unlimited = db.Column(db.Boolean, nullable=False, default=False)
  quantity = db.Column(db.Integer)

  project = db.relationship(
    "Project",
    back_populates="rewards"
  )

  backers = db.relationship(
    "Backer",
    back_populates="rewards",
    secondary="backer_rewards"
  )

  items = db.relationship(
    "RewardItem",
    back_populates="reward",
    cascade="all, delete-orphan"
  )


  def to_dict(self):
    return {
      "id": self.id,
      "projectId": self.project_id,
      "image": self.image,
      "title": self.title,
      "description": self.description,
      "shipping": self.shipping,
      "physicalItems": self.physical_items,
      "amount": self.amount,
      "unlimited": self.unlimited,
      "quantity": self.quantity,
      "deliveryDate": self.delivery_date,
      "items": [item.to_dict() for item in self.items],
      "backers": [backer.reward_to_dict() for backer in self.backers] if self.backers else ""
    }

def on_reward_delete(mapper, connection, target):
  remove_file_from_s3(target.image)
  return 'blah'

event.listen(Reward, 'before_delete', on_reward_delete)
