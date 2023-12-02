from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Reward, RewardItem, db, Project
from app.forms import RewardEditForm, RewardItemForm
from .aws_helper import get_unique_filename, upload_file_to_s3, remove_file_from_s3
from .helper_functions import user_owns

ri_routes = Blueprint('reward_items', __name__, url_prefix="/api/reward_items")

def validation_errors_to_error_messages(validation_errors):
  """
  Simple function that turns the WTForms validation errors into a simple list
  """
  errorMessages = []
  for field in validation_errors:
    for error in validation_errors[field]:
      errorMessages.append(f'{field} : {error}')
  return errorMessages


@ri_routes.route('/<int:id>')
def get_item(id):
  """Get Item by id"""
  item = RewardItem.query.get(id)

  if not item:
    return {'not_found': 'Item not found'}, 404

  return item.to_dict(), 200

@ri_routes.route('/<int:id>/edit', methods=['PUT'])
@login_required
def edit_item(id):
  """
  Updates a reward item's information
  """
  form = RewardItemForm()
  form['csrf_token'].data = request.cookies['csrf_token']
  item = RewardItem.query.get(id)
  reward = Reward.query.get(item.reward_id)
  project = Project.query.get(reward.project_id)

  if not item:
    return {'not_found': 'Reward Item not found'}, 404

  if not user_owns(project):
    return {'errors': 'Unauthorized'}, 403

  if form.validate_on_submit():
    data = form.data
    upload = None

    item_img = data['image']

    if item_img:
      old_img = item.image
      item_img.filename = get_unique_filename(item_img.filename)
      upload = upload_file_to_s3(item_img)
      if 'url' not in upload:
        return upload, 400
      if old_img:
        remove_file_from_s3(old_img)
    item.title=data['title']
    if upload:
      item.image=upload['url']
    item.quantity=data['quantity']

    db.session.commit()
    return item.to_dict(), 200
  return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@ri_routes.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_reward(id):
  """Delete an item from a reward"""
  item = RewardItem.query.get(id)
  reward = Reward.query.get(int(item.reward_id))
  project = Project.query.get(int(reward.project_id))
  # print('This is the user id ', item.reward_id)

  if not user_owns(project):
    print('This is the user id ', current_user.get_id(), project.user_id)
    return {'errors': 'Unauthorized'}, 403

  db.session.delete(item)
  db.session.commit()
  return {'message': 'Item deleted'}
