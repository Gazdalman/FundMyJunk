from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Reward, RewardItem, db, Project
from app.forms import RewardEditForm, RewardItemForm
from .aws_helper import get_unique_filename, upload_file_to_s3, remove_file_from_s3
from .helper_functions import user_owns

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


@reward_routes.route('/<int:id>')
def get_reward(id):
  """
  Gets a single reward by id
  """
  reward = Reward.query.get(id)

  if not reward:
    return {'not_found': 'Reward not found'}, 404

  return reward.to_dict()


@reward_routes.route('/<int:id>/items/new', methods=['POST'])
@login_required
def create_item(id):
  """
  Create a new item for a reward
  """
  form = RewardItemForm()
  form['csrf_token'].data = request.cookies['csrf_token']
  reward = Reward.query.get(id)
  project = Project.query.get(reward.project_id)

  if not reward:
    return {'not_found': 'Reward not found'}, 404

  if not user_owns(project):
    return {'errors': 'Unauthorized'}, 403


  if form.validate_on_submit():
    data = form.data
    upload = None
    image = data['image']

    if image:
      image.filename = get_unique_filename(image.filename)
      upload = upload_file_to_s3(image)
      if 'url' not in upload:
        return upload

    item = RewardItem(
      reward_id=id,
      title=data['title'],
      quantity=data['quantity'],
      image=upload['url']
    )
    db.session.add(item)
    db.session.commit()
    return item.to_dict()
  return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@reward_routes.route('/<int:id>/edit', methods=['PUT'])
@login_required
def edit_reward(id):
  """
  Updates a reward's information
  """
  form = RewardEditForm()
  form['csrf_token'].data = request.cookies['csrf_token']
  reward = Reward.query.get(id)
  project = Project.query.get(reward.project_id)

  if not reward:
    return {'not_found': 'Reward not found'}, 404

  if not user_owns(project):
    return {'errors': 'Unauthorized'}, 403

  if form.validate_on_submit():
    data = form.data
    img_upload = None

    reward_img = data['image']

    if reward_img:
      old_img = reward.image
      reward_img.filename = get_unique_filename(reward_img.filename)
      img_upload = upload_file_to_s3(reward_img)
      if 'url' not in img_upload:
        return img_upload, 400
      if old_img:
        remove_file_from_s3(old_img)
    reward.title=data['title']
    reward.description=data['description']
    if img_upload:
      reward.image=img_upload['url']
    reward.delivery_date=data['deliveryDate']
    reward.amount=data['amount']
    reward.unlimited=data['unlimited']
    reward.quantity=data['quantity']
    reward.physical_items=data['physicalItems']
    reward.shipping=data['shipping']

    db.session.commit()
    return reward.to_dict(), 200
  return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@reward_routes.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_reward(id):
  """
  Delete reward
  """
  reward = Reward.query.get(id)
  project = Project.query.get(reward.project_id)

  if not user_owns(project):
    return {'errors': 'Unauthorized'}, 403

  db.session.delete(reward)
  db.session.commit()
  return {'message': 'Reward deleted'}
