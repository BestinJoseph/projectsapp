from flask import Blueprint, render_template, redirect, url_for, flash, request
from projectsapp.forms import ProjectCreateForm
from projectsapp.extensions import db, Session
from projectsapp.models import User, Client, Project, ProjectSchema
from flask_login import current_user, login_required
from datetime import datetime

projects_blueprint = Blueprint('projects_blueprint', __name__, url_prefix="/projects")

@projects_blueprint.route('/')
@login_required
def projects() :
    session = Session()
    projects = session.query(Project).order_by(Project.id.desc())
    session.close()
    return render_template('projects.html', title="Projects", projects=projects)

@projects_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_project() :
    form = ProjectCreateForm()
    if form.validate_on_submit() :
        session = Session()
        # processing data from the form data
        form_data = {'project_name' : form.project_name.data, 'request_reference': form.request_reference.data, 'project_status': 'progress', 'client_id': int(form.client_id.data), 'pro_created_by': current_user.id}
        posted_project = ProjectSchema().load(form_data)
        project = Project(**posted_project, created_by=current_user.id)
        session.add(project)
        session.commit()
        session.close()
        flash('New Project created successfully', 'success')
        return redirect( url_for('projects_blueprint.projects') )
    return render_template('create_project.html', title="Projects", form=form)

@projects_blueprint.route('/<string:project_id>', methods=['GET'])
def single_project(project_id) :
    try :
        session = Session()
        project = session.query(Project).filter_by(project_id=project_id).first()
        # session.close()
        return render_template('single_project.html', title="Project", project=project)
    finally :
        session.close()