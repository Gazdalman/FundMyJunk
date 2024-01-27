from flask import Blueprint, jsonify, session, request
from sqlalchemy import or_
from app.models import User, db, UserProfile
from app.forms import LoginForm, SignUpForm, UserEditForm
from .aws_helper import get_unique_filename, upload_file_to_s3, remove_file_from_s3
from flask_login import current_user, login_user, logout_user, login_required

auth_routes = Blueprint('auth', __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': ['Unauthorized']}


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        user = User.query.filter(
            or_(User.email == form.data['cred'], User.username == form.data['cred'])).first()
        login_user(user)
        return user.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        upload = None
        image = form.data['image']

        if image:
            image.filename = get_unique_filename(image.filename)
            upload = upload_file_to_s3(image)
            if 'url' not in upload:
                return upload

        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            display_name=form.data['displayName']
        )
        db.session.add(user)

        user_profile = UserProfile(
            user_id=user.id
        )

        db.session.add(user_profile)

        db.session.commit()
        login_user(user)
        return user.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@auth_routes.route('/<int:id>/edit', methods=['PUT'])
@login_required
def edit_user(id):
    form = UserEditForm()
    user = User.query.get(id)
    if form.validate_on_submit():
        upload = None
        image = form.data['image']

        if image:
            image.filename = get_unique_filename(image.filename)
            upload = upload_file_to_s3(image)
            if 'url' not in upload:
                return upload

        user.profile_picture=form.data['image']
        user.display_name=form.data['displayName']
        user.biography=form.data['biography']
        user.private=form.data['private']
        db.session.commit()
        return user.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401

@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': ['Unauthorized']}, 401
