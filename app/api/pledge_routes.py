from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Project, Backer, BackerReward, Reward, db
from app.forms import PledgeForm
from .aws_helper import get_unique_filename, upload_file_to_s3, remove_file_from_s3
from .helper_functions import user_owns

pledge_routes = Blueprint('pledges', __name__, url_prefix="/api/pledges")

def validation_errors_to_error_messages(validation_errors):
  """
  Simple function that turns the WTForms validation errors into a simple list
  """
  errorMessages = []
  for field in validation_errors:
    for error in validation_errors[field]:
      errorMessages.append(f'{field} : {error}')
  return errorMessages

@pledge_routes.route('/')
@login_required
def get_user_pledges ():
  """
  Get all pledges for a user
  """
  pledges = Backer.query.filter(Backer.user_id == current_user.get_id()).all()

  return {f"{pledge.id}": pledge.to_dict() for pledge in pledges}

@pledge_routes.route('/<int:id>', methods=['PUT'])
@login_required
def edit_pledge(id):
  """
  Edit a pledge
  """
  form = PledgeForm()
  form['csrf_token'].data = request.cookies['csrf_token']

  pledge = Backer.query.get(id)

  if not pledge:
    return {'errors': ['Pledge does not exist']}, 404

  if not user_owns(pledge):
    return {'errors': ['You are not authorized to edit this pledge']}, 401

  project = Project.query.get(pledge.project_id)

  if form.validate_on_submit():
    db.session.delete(pledge)

    project.earned_today = project.earned_today - pledge.amount

    pledge = Backer(
      id = id,
      user_id = current_user.get_id(),
      project_id = project.id,
      amount = form.data['amount']
    )



    db.session.add(pledge)

    project.earned_today = project.earned_today + pledge.amount

    for reward in project.rewards:
      if reward.amount <= pledge.amount and (reward.unlimited or reward.quantity > 0):
        pledge.rewards.append(reward)
        if not reward.unlimited:
          reward.quantity = reward.quantity - 1

    db.session.commit()
    return pledge.to_dict()
  return {'errors': validation_errors_to_error_messages(form.errors)}, 401

@pledge_routes.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_pledge(id):
  """
  Delete a pledge
  """
  pledge = Backer.query.get(id)

  if not pledge:
    return {'errors': ['Pledge does not exist']}, 404

  if not user_owns(pledge):
    return {'errors': ['You are not authorized to delete this pledge']}, 401

  for reward in pledge.rewards:
    if not reward.unlimited:
      reward.quantity = reward.quantity + 1

  project = Project.query.get(pledge.project_id)
  project.earned_today = project.earned_today - pledge.amount

  db.session.delete(pledge)
  db.session.commit()
  
  return {'message': 'Pledge deleted'}, 200
