from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import Project

project_routes = Blueprint('projects', __name__, url_prefix="/api/projects")

def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages

@project_routes.route('/')
def get_all_projects():
  """
  Returns all projects
  """
  projects = Project.query.all()

  proj_dict = {project.id: project.to_dict() for project in projects}

  return proj_dict, 200
