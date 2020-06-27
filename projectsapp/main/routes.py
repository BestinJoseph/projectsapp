from flask import Blueprint, render_template, url_for, redirect
from projectsapp.models import Project

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/')
def home() :
    return render_template('home.html')

@main_blueprint.route('/about')
def about() :
    return render_template('about.html', title="About")