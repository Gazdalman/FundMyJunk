from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Project, Reward, db
from app.forms import RewardForm, RewardEditForm
from .aws_helper import get_unique_filename, upload_file_to_s3, remove_file_from_s3

reward_routes = Blueprint('rewards', __name__, url_prefix="/api/rewards")

def validation_errors_to_error_messages(validation_errors):
  """
  Simple function that turns the WTForms validation errors into a simple list
  """
  errorMessages = []
  for field in validation_errors:
    for error in validation_errors[field]:
      errorMessages.append(f'{field} : {error}')
  return errorMessages
