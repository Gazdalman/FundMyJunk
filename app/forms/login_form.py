from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User


def user_exists(form, field):
    # Checking if user exists
    cred = field.data
    user = User.query.filter(User.email == cred or User.username == cred).first()
    if not user:
        raise ValidationError('Email provided not found.')


def password_matches(form, field):
    # Checking if password matches
    password = field.data
    cred = form.data['cred']
    user = User.query.filter(User.email == cred or User.username == cred).first()
    if not user:
        raise ValidationError('No such user exists.')
    if not user.check_password(password):
        raise ValidationError('Password was incorrect.')


class LoginForm(FlaskForm):
    cred = StringField('cred', validators=[DataRequired(), user_exists])
    password = StringField('password', validators=[DataRequired(), password_matches])
