from .db import db, environment, SCHEMA, add_prefix_for_prod

class Reward(db.Model):
  __tablename__ = "rewards"

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("projects.id")))
  image = db.Column(db.String(50), nullable=False)
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

  items = db.relationship(
    "RewardItem",
    back_populates="reward"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "image": self.image,
      "title": self.title,
      "description": self.description,
      "shipping": self.shipping,
      "physicalItems": self.physical_items,
      "amount": self.amount,
      "unlimited": self.unlimited,
      "quantity": self.quantity,
      "deliveryDate": self.delivery_date,
      "items": [item.to_dict() for item in self.items]
    }
