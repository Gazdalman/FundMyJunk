from .db import db, environment, SCHEMA, add_prefix_for_prod

class UserProfile(db.Model):
  __tablename__ = 'user_profiles'

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey(
      add_prefix_for_prod('users.id')), nullable=False)
  bio = db.Column(db.String(500))
  first_name = db.Column(db.String(50))
  last_name = db.Column(db.String(50))
  location = db.Column(db.String(255))
  website = db.Column(db.String(255))
  private = db.Column(db.Boolean, default=True)
  profile_pic = db.Column(db.String(255))

  user = db.relationship(
      "User",
      back_populates="profile"
  )

  def to_dict(self):
    return {
        "id": self.id,
        "userId": self.user_id,
        "bio": self.bio,
        "firstName": self.first_name,
        "lastName": self.last_name,
        "private": self.private,
        "profilePic": self.profile_pic,
        "location": self.location,
        "website": self.website,
    }
