from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from app.models import User
from app.api.aws_helper import ALLOWED_IMG_EXTENSIONS


def user_exists(form, field):
    # Checking if user exists
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('Email address is already in use.')


def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')


class SignUpForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), Length(min=5,max=40), username_exists])
    email = StringField('email', validators=[DataRequired(), user_exists])
    firstName = StringField('first name', validators=[DataRequired(), Length(min=3, max=50)])
    lastName = StringField('last name', validators=[Length(min=0, max=50)])
    password = StringField('password', validators=[DataRequired(), Length(min=8)])
    displayName = StringField('displayName', validators=[Length(min=0,max=50)])
    private = BooleanField('private')
    biography = TextAreaField('biography', validators=[Length(max=1000)])
    image = FileField('profile pic', validators=[FileAllowed(ALLOWED_IMG_EXTENSIONS)])
