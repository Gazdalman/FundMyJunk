from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, FileField, DateField, BooleanField
from wtforms.validators import Length
from app.api.aws_helper import ALLOWED_IMG_EXTENSIONS

class ProfileEditForm(FlaskForm):
  displayName = StringField('display name', validators=[Length(max=50)])
  image = FileField('profile pic', validators=[FileAllowed(ALLOWED_IMG_EXTENSIONS)])
  biography = TextAreaField('biography', validators=[Length(max=1000)])
  private = BooleanField('private')
