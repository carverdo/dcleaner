"""
JUST A SAMPLE SCRIPT.
NEEDS TO BE MODIFIED FOR YOUR PARTICULAR DB/MODEL STRUCTURE.
"""
from flask.ext.sqlalchemy import SQLAlchemy
from app import create_app
from app.db_models import Member
from config_vars import INITIALLY_ACTIVE, RIBCAGE_KEY01, RIBCAGE_KEY02
from datetime import datetime


def init_data():
    """Simple set-up"""
    tmp_app = create_app('development')
    db = SQLAlchemy(tmp_app)
    if db.session.query(Member).count() == 0:
        member1 = Member(
            firstname=RIBCAGE_KEY01[0], surname=RIBCAGE_KEY01[1],
            email=RIBCAGE_KEY01[2], password=RIBCAGE_KEY01[3],
            adminr=True, active=INITIALLY_ACTIVE,
            confirmed=True, first_log=datetime.utcnow(),
            last_log=datetime.utcnow(), logins=1
        )
        member2 = Member(
            firstname=RIBCAGE_KEY02[0], surname=RIBCAGE_KEY02[1],
            email=RIBCAGE_KEY02[2], password=RIBCAGE_KEY02[3],
            adminr=True, active=INITIALLY_ACTIVE,
            confirmed=True, first_log=datetime.utcnow(),
            last_log=datetime.utcnow(), logins=1
        )
        db.session.add_all([member1, member2])
    db.session.commit()

if __name__ == '__main__':
    init_data()
