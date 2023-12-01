from .db import db, environment, SCHEMA, add_prefix_for_prod

class Story(db.Model):
  __tablename__ = "stories"

  if environment == "production":
    __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.INTEGER, primary_key=True)
  project_id = db.Column(db.INTEGER, db.ForeignKey(add_prefix_for_prod("projects.id")), nullable=False)
  ai = db.Column(db.Boolean, nullable=False, default=False)
  story_text = db.Column(db.String(2000), nullable=False)
  risks_challenges = db.Column(db.String(2500), nullable=False)

  project = db.relationship(
    "Project",
    back_populates="story"
  )

  def to_dict(self):
    return {
      "id": self.id,
      "ai": self.ai,
      "text": self.story_text,
      "risks_challenges": self.risks_challenges
    }
