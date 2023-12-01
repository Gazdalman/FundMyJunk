from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, FloatField, TextAreaField, FileField, DateField, BooleanField
from wtforms.validators import DataRequired, Length
from app.api.aws_helper import ALLOWED_IMG_EXTENSIONS, ALLOWED_VID_EXTENSIONS

class ProjectEditForm(FlaskForm):
  title = StringField('title', validators=[DataRequired(), Length(max=60)])
  subtitle = TextAreaField('subtitle', validators=[DataRequired(), Length(max=135)])
  location = StringField('location', validators=[DataRequired()])
  image = FileField('image', validators=[FileAllowed(list(ALLOWED_IMG_EXTENSIONS))])
  video = FileField('video', validators=[FileAllowed(ALLOWED_VID_EXTENSIONS)])
  type = StringField('type', validators=[DataRequired()])
  goal = FloatField('goal', validators=[DataRequired()])
  mainCategory = StringField('main cat', validators=[DataRequired()])
  mainSubcat = StringField('main cat', validators=[DataRequired()])
  secondCat = StringField('main cat')
  secondSubcat = StringField('main cat')
  launchDate = DateField('launch')
  endDate = DateField('end')
  launched = BooleanField('launched')
