"""
Updated to allow for the config database choices.
Creation of our main tools, app and db.
Imports views for run.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager, logout_user, login_required
login_manager = LoginManager()
login_manager.login_view = 'home'
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # initialising our app
    config[config_name].init_app(app)
    # db.init_app(app)
    login_manager.init_app(app)
    db = SQLAlchemy(app)
    return app, db


# =================
# CREATE PACKAGE
# =================
db = SQLAlchemy()
from flask import Flask
app = Flask(__name__)
app.secret_key = 's3cr3t'
app, db = create_app('development')
from app.main import views, view_errors

# =================
# BUILD MANAGER (for cmd handling)
# here we only add the databse commands
# we don't yet .run() as this locks the commands in
# =================
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)

# =================
# Toolbar Extension
# =================
toolbar = DebugToolbarExtension(app)
