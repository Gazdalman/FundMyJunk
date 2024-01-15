from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError

class StoryForm(FlaskForm):
  ai = BooleanField('ai')
  storyText = TextAreaField('story text', validators=[DataRequired('Story text is required'), Length(max=2000)])
  risksChallenges = TextAreaField('risks', validators=[DataRequired('Risks are required'), Length(max=2500)])
