from .db import db, environment, SCHEMA, add_prefix_for_prod


class Backer(db.Model):
    __tablename__ = 'backers'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(
        add_prefix_for_prod("projects.id")), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        add_prefix_for_prod('users.id')), nullable=False)
    amount = db.Column(db.FLOAT, nullable=False)

    project = db.relationship(
        "Project",
        back_populates="backers"
    )

    user = db.relationship(
        "User",
        back_populates="backed"
    )

    rewards = db.relationship(
        "Reward",
        back_populates="backers",
        secondary="backer_rewards"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "projectId": self.project_id,
            "userId": self.user_id,
            "amount": self.amount,
            "rewards": [reward.to_dict() for reward in self.rewards]
        }

    def reward_to_dict(self):
        return {
            "id": self.id,
            "projectId": self.project_id,
            "userId": self.user_id,
            "amount": self.amount,
        }
