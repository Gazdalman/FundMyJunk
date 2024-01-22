from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms.validators import DataRequired, Length, ValidationError

class PledgeForm(FlaskForm):
  amount = FloatField('amount', validators=[DataRequired('Amount is required')])
