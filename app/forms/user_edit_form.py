from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, FileField, DateField, BooleanField
from wtforms.validators import Length, ValidationError
from app.api.aws_helper import ALLOWED_IMG_EXTENSIONS
from app.models import User


# def name_taken(form, field):
#   displayName = field.data
#   user = User.query.filter(User.displayName == displayName).first()
#   if user:
#     raise ValidationError('Display name is already in use.')

class UserEditForm(FlaskForm):
  displayName = StringField('display name', validators=[Length(max=50)])
  password = StringField('password', validators=[Length(min=8, max=50)])
