from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import User
from .aws_helper import get_unique_filename, upload_file_to_s3


user_routes = Blueprint('users', __name__)

@user_routes.route('/')
@login_required
def users():
    """
    Query for all users and returns them in a list of user dictionaries
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
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
