from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    hashed_password = db.Column(db.String(255), nullable=False)
    user_credit = db.Column(db.FLOAT, default=10000)
    display_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=(datetime.now()))

    projects = db.relationship(
        "Project",
        back_populates="user"
    )

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        safe_user = {
            'id': self.id,
            'firstName': self.first_name,
            'username': self.username,
            'email': self.email,
            'userCredit': self.user_credit,
            'displayName': self.display_name if self.display_name else self.username,
            'created_at': self.created_at
        }
        if self.last_name:
            safe_user['lastName'] = self.last_name
        return safe_user
