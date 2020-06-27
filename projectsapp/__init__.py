from flask import Flask

from sassutils.wsgi import SassMiddleware

from .extensions import db, bcrypt, login_manager, Base, engine, datepicker # Base and engine from sql
from projectsapp.clients.routes import clients_blueprint
from projectsapp.main.routes import main_blueprint
from projectsapp.projects.routes import projects_blueprint
from projectsapp.auth.routes import auth_blueprint
from projectsapp.proposals.routes import proposal_blueprint
from projectsapp.tests.routes import test_blueprint

def create_app(config_file='settings.py') :

    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'projectsapp': { 'sass_path':'static/sass', 'css_path':'static/css', 'strip_extension': True}
    })
    
    bcrypt.init_app(app)
    db.init_app(app)
    Base.metadata.create_all(engine) # sql info
    login_manager.init_app(app)
    datepicker.init_app(app)

    app.register_blueprint(clients_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(proposal_blueprint)
    app.register_blueprint(test_blueprint)

    return app