"""
This is just a way of adding commands that we can use in the cmd module.

We already created manager (in the init) so that it can init/up/downgrade the db;
(We can run all of the db creation / migration functions from here if we wish.)

Now we add other objects so we can access via cmd line;
e.g. app, db, Member etc.

0. Hash out references to debug in the __init__; seems like the ext vs - thing annoys it
1.Activate your venv (venv\scripts\activate).
2. Then (just like with db_create_migrate):
<venv> > python manager.py shell

I could only get to run by killing the usual
if __name__ == ...
(since cmd doesn't recognise)

NB Sometimes it doesn't like the flask.ext.package; just comment out.

Get rid of manager.run() and you can play around in the gui.
"""
__author__ = 'donal'
__project__ = 'dcleaner'
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Shell
from run import app
from app import db
from app.db_models import Member

# =================
# BUILD MANAGER (for cmd handling)
# =================
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)
# ADD SHELL COMMANDS
def _make_context():
    return dict(app=app, db=db, Member=Member, use_ipython=False)
manager.add_command('shell', Shell(make_context=_make_context))

# IMPORTANT! (updates manager, locks the commands in)
manager.run()