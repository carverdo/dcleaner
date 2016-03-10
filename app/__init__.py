"""
Updated to allow for the config database choices.
Creation of our main tools, app and db.
Imports views for run.

# I've set up using blueprints (but not yet sure how much use they are).
They allow "routes to be defined in the global scope" after the app is created.

In practice this means we can create many "main" directories each with its
own forms and views as neither forms nor views has any knowledge of 'app'.
That linkage is registered/happens below.
"""
__author__ = 'donal'
__project__ = 'dcleaner'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from config import config
from config_vars import LOGOUT
from logs.LogGenerator import GenLogger

# ================
# KEEP OUTSIDE create_app - we import elsewhere
# ================
# csrf = CsrfProtect()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'log_auth.signin'
login_manager.session_protection = 'strong'
toolbar = DebugToolbarExtension()
# Moment = Moment()  # local/client time (suspect this is slow)
# cache = Cache()
lg = GenLogger(LOGOUT)


def create_app(config_name):
    app = Flask(__name__)
    # csrf.init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    if app.config['DEBUG']:
        toolbar.init_app(app)
    # moment = Moment.init_app(app)
    # cache.init_app(app, config={'CACHE_TYPE': 'simple'})

    from .log_auth import log_auth as la_blueprint
    app.register_blueprint(la_blueprint)

    from .proj import proj as proj_blueprint
    app.register_blueprint(proj_blueprint)

    from .updown import updo as updo_blueprint
    app.register_blueprint(updo_blueprint)

    from .log_records import log_recs as recs_blueprint
    app.register_blueprint(recs_blueprint)
    return app
