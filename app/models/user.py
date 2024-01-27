from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .likes import Like


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=(datetime.now()))

    projects = db.relationship(
        "Project",
        back_populates="user"
    )

    liked_projects = db.relationship(
        "Project",
        secondary=Like.__table__,
        back_populates="liked_users"
    )

    backed = db.relationship(
        "Backer",
        back_populates="user"
    )

    profile = db.relationship(
        "UserProfile",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_rewards(self):
        rewards = []
        for backer in self.backed:
            for reward in backer.rewards:
                rewards.append(reward)
        return rewards

    def to_dict(self):
        safe_user = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'displayName': self.display_name if self.display_name else self.username,
            'created_at': self.created_at,
            'rewards': [reward.to_dict() for reward in self.get_rewards()],
            'liked': {project.id: project.to_dict() for project in self.liked_projects},
            'backed': [backer.user_to_dict() for backer in self.backed],
            'profile': self.profile[0].to_dict() if self.profile else None
        }

        # if self.last_name:
        #     safe_user['lastName'] = self.last_name
        return safe_user
