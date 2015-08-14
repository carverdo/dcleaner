"""
We import our empty db and write our model changes to it.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from flask.ext.login import UserMixin
from config_vars import MAX_COL_WIDTHS, ADMIN_USER, INITIALLY_ACTIVE
from datetime import datetime

# ==============================
# DATABASE STRUCTURE
# ==============================
class Member(UserMixin, db.Model):
    """Simple member / user definition"""
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(MAX_COL_WIDTHS), nullable=False)
    surname = Column(String(MAX_COL_WIDTHS), nullable=False, unique=True)
    email = Column(String(MAX_COL_WIDTHS), nullable=False, unique=True)
    pwdhash = Column(String, nullable=False)
    adminr = Column(Boolean)
    active = Column(Boolean)
    first_log = Column(DateTime(), default=datetime.utcnow)
    last_log = Column(DateTime(), default=datetime.utcnow)
    logins = Column(Integer)

    def __init__(self, firstname, surname, email, password,
                 adminr=ADMIN_USER, active=INITIALLY_ACTIVE,
                 first_log=datetime.utcnow(), last_log=datetime.utcnow(), logins=1):
        self.firstname = firstname.title()
        self.surname = surname.title()
        self.email = email.lower()
        self.set_password(password)
        self.adminr = adminr
        self.active = active
        self.first_log = first_log
        self.last_log = last_log
        self.logins = logins

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    # Next 4 all for flask-login
    def is_authenticated(self):
        """True: if exist, they are authenticated"""
        return True
    def is_active(self):
        """Extra protection: we can determine/toggle"""
        return self.active
    def is_anonymous(self):
        """False: not allowed"""
        return False
    def get_id(self):
        return unicode(self.id)

    def ping(self):
        self.last_log = datetime.utcnow()
        self.logins += 1
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<{0} {1}>'.format(self.surname, self.email)


# flask-login needs this definition
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))


if __name__ == '__main__':
    mem = Member('pat','brok','PB','fish', 0)
    print mem
    print mem.pwdhash
    print mem.check_password('Fish'), mem.check_password('fish')
