from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Project, Reward, Backer, BackerReward, Story, db
from app.forms import ProjectForm, PledgeForm, ProjectEditForm, RewardForm, StoryForm, ImageForm
from .aws_helper import get_unique_filename, upload_file_to_s3, remove_file_from_s3
from .helper_functions import user_owns
from datetime import datetime
from sqlalchemy import or_

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


@project_routes.route("/current")
@login_required
def get_curr_user_projects():
    projects = Project.query.filter(Project.user_id == current_user.get_id()).all()

    return {f"{project.id}": project.to_dict() for project in projects}

@project_routes.route("/users/<int:id>")
def get_user_projects(id):
    projects = Project.query.filter(Project.user_id == id, Project.launched == True ).all()
    return {f"{project.id}": project.to_dict() for project in projects}

@project_routes.route('/')
def get_home_projects():
    """
    Returns home page projects
    """

    projects = Project.query.filter(Project.launch_date <= datetime.utcnow(
    ), Project.end_date >= datetime.utcnow()).order_by(Project.earned_today.desc()).paginate(page=1, per_page=12)

    proj_arr = [project.to_dict() for project in projects]

    return proj_arr, 200


@project_routes.route('/search')
def query_projects():
    """
    Returns all projects
    """
    # Grab the pagination and keyword from the query
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    keyword = request.args.get('keyword', None)

    if keyword:
        projects = Project.query.filter(
            Project.launch_date <= datetime.utcnow(),
            Project.end_date >= datetime.utcnow(),
            or_(
                Project.title.ilike(f"%{keyword}%"),
                Project.main_category.ilike(f"%{keyword}%"),
                Project.main_subcat.ilike(f"%{keyword}%"),
                Project.second_cat.ilike(f"%{keyword}%"),
                Project.second_subcat.ilike(f"%{keyword}%"),
                Project.subtitle.ilike(f"%{keyword}%"),
            )).paginate(page=page, per_page=per_page)

    else:
        projects = Project.query.paginate(page=page, per_page=per_page)

    return [project.to_dict() for project in projects], 200


@project_routes.route('/<int:id>')
def get_one(id):
    """
    Get a single project by id
    """
    project = Project.query.get(id)

    if not project:
        return {'not_found': 'Project was not found'}, 404

    return project.to_dict(), 200


@project_routes.route('/search/<string:query>')
@project_routes.route('/new', methods=['POST'])
@login_required
def create_project():
    """
    Creates a new Project associated with the current user
    """
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
            end_date=data['endDate'],
            launched=data['launched']
        )

        db.session.add(project)
        db.session.commit()

        return project.to_dict(), 200
    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@project_routes.route('/<int:id>/story', methods=['PUT', 'POST'])
@login_required
def create_story(id):
    """
    Create or edit a story for a project
    """
    form = StoryForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    project = Project.query.get(id)

    if not project:
        return {'not_found': 'Project was not found'}, 404

    if not user_owns(project):
        return {'errors': 'Unauthorized'}, 403

    if form.validate_on_submit():
        data = form.data
        story = Story(
            project_id=id,
            ai=data['ai'],
            story_text=data['storyText'],
            risks_challenges=data['risksChallenges']
        )
        db.session.add(story)
        db.session.commit()
        return story.to_dict()

    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@project_routes.route('/<int:id>/pledge', methods=['POST'])
@login_required
def create_pledge(id):
    """
    Create a pledge on a project
    """

    total = 0

    form = PledgeForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    project = Project.query.get(id)
    if not project:
        return {'not_found': 'Project was not found'}

    if user_owns(project):
        return {'errors': 'You own this bro...'}, 403

    past_pledge = Backer.query.filter(
        Backer.project_id == id, Backer.user_id == current_user.get_id()).first()

    old_id = None

    if form.validate_on_submit():
        if past_pledge:
            total = past_pledge.amount
            old_id = past_pledge.id
            project.earned_today = (
                project.earned_today - total) if project.earned_today else 0

            if len(past_pledge.rewards):
                for reward in past_pledge.rewards:
                    past_pledge.rewards.remove(reward)
                    if not reward.unlimited:
                        reward.quantity = reward.quantity + 1
            db.session.delete(past_pledge)

        data = form.data

        if old_id:
            pledge = Backer(
                id=old_id,
                project_id=id,
                user_id=current_user.get_id(),
                amount=data['amount'] + total
            )
        else:
            pledge = Backer(
                project_id=id,
                user_id=current_user.get_id(),
                amount=data['amount'] + total
            )
        db.session.add(pledge)

        project.earned_today = (
            project.earned_today + pledge.amount) if project.earned_today else pledge.amount

        for reward in project.rewards:
            if reward.amount <= pledge.amount and (reward.unlimited or reward.quantity > 0):
                pledge.rewards.append(reward)
                if not reward.unlimited:
                    reward.quantity = reward.quantity - 1

        db.session.commit()
        return pledge.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@project_routes.route('/<int:id>/like', methods=['POST'])
@login_required
def like_project(id):
    """
    Like a project
    """
    project = Project.query.get(id)

    message = 'Project liked'

    if not project:
        return {'not_found': 'Project was not found'}

    if user_owns(project):
        return {'errors': 'You own this bro...'}, 403

    if project in current_user.liked_projects:
        current_user.liked_projects.remove(project)
        message = 'Project unliked'
    else:
        current_user.liked_projects.append(project)
        message = 'Project liked'

    db.session.commit()
    return {"message": message}


@project_routes.route('/<int:id>/rewards/new', methods=['POST'])
@login_required
def create_reward(id):
    """
    Create a reward on a project
    """
    form = RewardForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    project = Project.query.get(id)
    if not project:
        return {'not_found': 'Project was not found'}

    if not user_owns(project):
        return {'errors': 'Unauthorized'}, 403

    if form.validate_on_submit():
        data = form.data

        img = data['image']
        img.filename = get_unique_filename(img.filename)
        upload = upload_file_to_s3(img)

        if 'url' not in upload:
            return upload

        reward = Reward(
            project_id=id,
            image=upload['url'],
            title=data['title'],
            description=data['description'],
            physical_items=data['physicalItems'],
            shipping=data['shipping'],
            delivery_date=data['deliveryDate'],
            amount=data['amount'],
            unlimited=data['unlimited'],
            quantity=data['quantity']
        )
        db.session.add(reward)
        db.session.commit()
        return reward.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@project_routes.route('/<int:id>/edit', methods=['PUT'])
@login_required
def edit_project(id):
    """
    Updates the information on a project
    """
    form = ProjectEditForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    project = Project.query.get(id)
    if not project:
        return {'not_found': 'Product was not found'}, 404

    if not user_owns(project):
        return {'errors': 'Unauthorized'}, 403

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
            if old_img:
                remove_file_from_s3(old_img)

        if proj_vid:
            old_vid = project.video
            proj_vid.filename = get_unique_filename(proj_vid.filename)
            vid_upload = upload_file_to_s3(proj_vid)

            if 'url' not in vid_upload:
                return vid_upload, 400
            if old_vid:
                remove_file_from_s3(old_vid)

        if errs:
            print(errs)
            return errs, 400

        project.title = data['title']
        project.subtitle = data['subtitle']
        project.location = data['location']
        if img_upload:
            project.image = img_upload['url']
        if vid_upload:
            project.video = vid_upload['url']
        project.type = data['type']
        project.goal = data['goal']
        project.main_category = data['mainCategory']
        project.main_subcat = data['mainSubcat']
        project.second_cat = data['secondCat']
        project.second_subcat = data['secondSubcat']
        project.launch_date = data['launchDate']
        project.end_date = data['endDate']

        db.session.commit()
        return project.to_dict(), 200
    return {'errors': validation_errors_to_error_messages(form.errors)}, 400


@project_routes.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete_project(id):
    """Deletes a project"""
    project = Project.query.get(id)
    if not project:
        return {'not_found': 'Product was not found'}, 404

    if not user_owns(project):
        return {'errors': 'Unauthorized'}, 403

    db.session.delete(project)
    db.session.commit()
    return {'message': 'Project deleted'}


@project_routes.route("/add_logo", methods=['POST'])
def logo_add():
    form = ImageForm()
    image = form.data['image']
    image.filename = get_unique_filename(image.filename)
    img_upload = upload_file_to_s3(image)
    return 'banaba'
