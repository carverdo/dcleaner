"""
JUST A SAMPLE SCRIPT.
NEEDS TO BE MODIFIED FOR YOUR PARTICULAR DB/MODEL STRUCTURE.
"""
from flask.ext.sqlalchemy import SQLAlchemy
from app import create_app
from app.db_models import Member # RELEVANT TABLES
from config_vars import INITIALLY_ACTIVE
from datetime import datetime


def init_data():
    """Simple set-up"""
    tmp_app = create_app('development')
    db = SQLAlchemy(tmp_app)
    if db.session.query(Member).count() == 0:
        donal = Member(firstname='donal', surname='carville', email='d@gmail.com',
                       password='dash', adminr=True, active=INITIALLY_ACTIVE, confirmed=True,
                       first_log=datetime.utcnow(), last_log=datetime.utcnow(), logins=1)
        matt = Member(firstname='matt', surname='sheridan', email='m@gmail.com',
                      password='mash', adminr=True, active=INITIALLY_ACTIVE, confirmed=True,
                       first_log=datetime.utcnow(), last_log=datetime.utcnow(), logins=1)
        db.session.add_all([donal, matt])
    db.session.commit()

if __name__ == '__main__':
    init_data()
