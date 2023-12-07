from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, IntegerField, FloatField, TextAreaField, BooleanField, FileField, DateField
from wtforms.validators import DataRequired, Length, ValidationError
from app.api.aws_helper import ALLOWED_IMG_EXTENSIONS

class ImageForm(FlaskForm):
  image = FileField('image')
