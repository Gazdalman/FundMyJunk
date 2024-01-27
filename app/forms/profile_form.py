from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, FloatField, TextAreaField, FileField, DateField, BooleanField
from wtforms.validators import DataRequired, Length
from app.api.aws_helper import ALLOWED_IMG_EXTENSIONS, ALLOWED_VID_EXTENSIONS

class UserProfileForm(FlaskForm):
  bio = TextAreaField('bio', validators=[Length(max=500)])
  location = StringField('location', validators=[Length(max=50)])
  first_name = StringField('firstName', validators=[Length(max=50)])
  last_name = StringField('lastName', validators=[Length(max=50)])
  website = StringField('website', validators=[Length(max=255)])
  private = BooleanField('private')
  profile_pic = FileField('profilePic', validators=[FileAllowed(list(ALLOWED_IMG_EXTENSIONS))])
