from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Reward, RewardItem, db
from app.forms import RewardEditForm, RewardItemForm
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


# @reward_routes.route('/<int:id>/items/new')
# @login_required
# def create_item(id):
#   form = RewardItemForm()
#   form['csrf_token'].data = request.cookies['csrf_token']
#   reward = Reward.query.get(id)

#   if not reward:
#     return {'not_found': 'Reward not found'}, 404


@reward_routes.route('/<int:id>/edit', methods=['PUT'])
@login_required
def edit_reward(id):
  """
  Updates a reward's information
  """
  form = RewardEditForm()
  form['csrf_token'].data = request.cookies['csrf_token']
  reward = Reward.query.get(id)

  if not reward:
    return {'not_found': 'Reward not found'}, 404

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
