"""
This runs pretty much automatically, but some tailoring is required here to
ensure it matches the requirements of our project.
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
lg = GenLogger(LOGOUT)
login_manager = LoginManager()
login_manager.login_view = 'log_auth.signin'
login_manager.session_protection = 'strong'
toolbar = DebugToolbarExtension()
# Moment = Moment()  # local/client time (suspect this is slow)
# cache = Cache()


def create_app(config_name):
    app = Flask(__name__)
    # csrf.init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    if app.config['DEBUG']: toolbar.init_app(app)
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
