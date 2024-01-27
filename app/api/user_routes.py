from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import User, db, UserProfile
from app.forms import UserEditForm, ImageForm
from .aws_helper import get_unique_filename, upload_file_to_s3


user_routes = Blueprint('users', __name__)

def validation_errors_to_error_messages(validation_errors):
  """
  Simple function that turns the WTForms validation errors into a simple list
  """
  errorMessages = []
  for field in validation_errors:
    for error in validation_errors[field]:
      errorMessages.append(f'{field} : {error}')
  return errorMessages

@user_routes.route('/')
@login_required
def users():
  """
  Query for all users and returns them in a list of user dictionaries
  """
  users = User.query.all()
  return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
# @login_required
def user(id):
  """
  Query for a user by id and returns that user in a dictionary
  """
  user = User.query.get(id)
  if not user:
    return {'not_found': 'User not found'}, 404
  return user.to_dict()

@user_routes.route('/current')
@login_required
def curr_user():
  user = User.query.get(current_user.get_id())

  return user.to_dict()

# @user_routes.route('/<int:id>/edit', methods=['PUT'])
# @login_required
# def edit_user(id):
#   form = UserEditForm()
#   user = User.query.get(id)
#   if form.validate_on_submit():
#     upload = None
#     image = form.data['image']

#     if image:
#       image.filename = get_unique_filename(image.filename)
#       upload = upload_file_to_s3(image)
#       if 'url' not in upload:
#         return upload

#       user.profile_picture=form.data['image']
#       user.display_name=form.data['displayName']
#       user.biography=form.data['biography']
#       user.private=form.data['private']
#       db.session.commit()
#       return user.to_dict()
#   return {'errors': validation_errors_to_error_messages(form.errors)}, 401
