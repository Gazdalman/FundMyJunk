from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import IntegerField, FileField, StringField
from wtforms.validators import DataRequired, Length
from app.api.aws_helper import ALLOWED_IMG_EXTENSIONS

class RewardItemForm(FlaskForm):
  title = StringField('title', validators=[DataRequired("Title is required"), Length(min=3,max=50)])
  quantity = IntegerField('quantity', validators=[DataRequired()])
  image = FileField('image', validators=[FileAllowed(ALLOWED_IMG_EXTENSIONS)])
