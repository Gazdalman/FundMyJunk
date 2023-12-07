from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Story, db, Project
from app.forms import StoryForm
from .helper_functions import user_owns

story_routes = Blueprint('stories', __name__, url_prefix="/api/stories")

def validation_errors_to_error_messages(validation_errors):
  """
  Simple function that turns the WTForms validation errors into a simple list
  """
  errorMessages = []
  for field in validation_errors:
    for error in validation_errors[field]:
      errorMessages.append(f'{field} : {error}')
  return errorMessages

@story_routes.route('/<int:id>')
@login_required
def get_story(id):
  """Get a specific story by id"""
  story = Story.query.get(id)

  if not story:
    return {'not_found': 'Story not found'}, 404

  return story.to_dict()


@story_routes.route('/<int:id>/edit', methods=['PUT'])
@login_required
def edit_story(id):
  """Update a story"""
  form = StoryForm()
  form['csrf_token'].data = request.cookies['csrf_token']
  story = Story.query.get(id)
  project = Project.query.get(story.project_id)
  if not story:
    return {'not_found': 'Story not found'}, 404

  if not user_owns(project):
    return {'errors': 'Unauthorized'}, 403

  if form.validate_on_submit():
    data = form.data

    story.ai = data['ai']
    story.story_text = data['storyText']
    story.risks_challenges = data['risksChallenges']

    db.session.commit()
    return story.to_dict()
  return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@story_routes.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_story(id):
  """Delete a story"""
  story = Story.query.get(id)
  project = Project.query.get(story.project_id)

  if not story:
    return {'not_found': 'Story not found'}, 404

  if not user_owns(project):
    return {'errors': 'Unauthorized'}, 403

  db.session.delete(story)
  db.session.commit()
  return {'message': 'Story deleted'}
