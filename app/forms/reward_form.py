from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, IntegerField, FloatField, TextAreaField, BooleanField, FileField, DateField
from wtforms.validators import DataRequired, Length, ValidationError
from app.api.aws_helper import ALLOWED_IMG_EXTENSIONS

def quantity_check(form, field):
  quantity = field.data
  unlimited = form.data['unlimited']
  if not unlimited:
    if not quantity:
      raise ValidationError('Quantity must be provided in not unlimited')


class RewardForm(FlaskForm):
  image = FileField('image', validators=[FileRequired('You must upload an image for your reward'), FileAllowed(list(ALLOWED_IMG_EXTENSIONS))])
  title = StringField('title', validators=[DataRequired('Title is required'), Length(min=3,max=50)])
  description = TextAreaField('description', validators=[Length(max=2000,message='Description must be between 3 to 2000 characters')])
  physicalItems = BooleanField('physical items')
  shipping = StringField('shipping', validators=[DataRequired('Shipping is required')])
  deliveryDate = DateField('delivery', validators=[DataRequired('Delivery date is required')])
  amount = FloatField('reward amount', validators=[DataRequired('Amount is required')])
  unlimited = BooleanField('unlimited')
  quantity = IntegerField('quantity', validators=[quantity_check])
