from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length
from api.aws_helper import ALLOWED_IMG_EXTENSIONS, ALLOWED_VID_EXTENSIONS

class ProjectForm(FlaskForm):
  title = StringField('title', validators=[DataRequired(), Length(max=60)])
  
