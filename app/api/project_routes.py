from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Project, User, db
from app.forms import ProjectForm, ProjectEditForm
from .aws_helper import get_unique_filename, upload_file_to_s3, remove_file_from_s3

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


@project_routes.route('/<int:id>')
def get_one(id):
  project = Project.query.get(id)

  if not project:
    return {'not_found': 'Project was not found'}, 404

  return project.to_dict(), 200


@project_routes.route('/new', methods=['POST'])
@login_required
def create_project():
  form = ProjectForm()
  form['csrf_token'].data = request.cookies['csrf_token']

  if form.validate_on_submit():
    data = form.data

    # Initialize an empty errs list
    errs = []

    # Initialize a video upload variable to check against later
    vid_upload = None

    # Pull in the image and video from the form
    proj_img = data['image']
    proj_vid = data['video']

    # Change the file name on the image and then upload
    proj_img.filename = get_unique_filename(proj_img.filename)
    img_upload = upload_file_to_s3(proj_img)
    if 'url' not in img_upload:
      errs = [img_upload]

    if proj_vid:
      proj_vid.filename = get_unique_filename(proj_vid.filename)
      vid_upload = upload_file_to_s3(proj_vid)

      if 'url' not in vid_upload:
        errs.append(vid_upload)

    if errs:
      print(errs)
      return errs, 400

    project = Project(
      user_id=current_user.get_id(),
      title=data['title'],
      subtitle=data['subtitle'],
      location=data['location'],
      image=img_upload['url'],
      video=vid_upload['url'] if vid_upload else None,
      type=data['type'],
      goal=data['goal'],
      main_category=data['mainCategory'],
      main_subcat=data['mainSubcat'],
      second_cat=data['secondCat'],
      second_subcat=data['secondSubcat'],
      launch_date=data['launchDate'],
      end_date=data['endDate']
    )

    db.session.add(project)
    db.session.commit()

    return project.to_dict(), 200
  return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@project_routes.route('/<int:id>/edit', methods=['PUT'])
@login_required
def edit_project(id):
  form = ProjectForm()
  form['csrf_token'].data = request.cookies['csrf_token']
  project = Project.query.get(id)
  if not project:
    return {'not_found': 'Product was not found'}, 404

  if form.validate_on_submit():
    data = form.data
    errs = []
    vid_upload = None
    img_upload = None

    proj_img = data['image']
    proj_vid = data['video']

    if proj_img:
      old_img = project.image
      proj_img.filename = get_unique_filename(proj_img.filename)
      img_upload = upload_file_to_s3(proj_img)
      if 'url' not in img_upload:
        return img_upload, 400
      remove_file_from_s3(old_img)

    if proj_vid:
      old_vid = project.video
      proj_vid.filename = get_unique_filename(proj_vid.filename)
      vid_upload = upload_file_to_s3(proj_vid)

      if 'url' not in vid_upload:
        return vid_upload, 400
      remove_file_from_s3(old_vid)

    if errs:
      print(errs)
      return errs, 400

    project.title=data['title']
    project.subtitle=data['subtitle']
    project.location=data['location']
    if img_upload:
      project.image=img_upload['url']
    if vid_upload:
      project.video=vid_upload['url']
    project.type=data['type']
    project.goal=data['goal']
    project.main_category=data['mainCategory']
    project.main_subcat=data['mainSubcat']
    project.second_cat=data['secondCat']
    project.second_subcat=data['secondSubcat']
    project.launch_date=data['launchDate']
    project.end_date=data['endDate']

    db.session.commit()
    return project.to_dict(), 200
  return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@project_routes.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_project(id):
  project = Project.query.get(id)
  db.session.delete(project)
  db.session.commit()
  return {'message': 'Project deleted'}
