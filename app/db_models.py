"""
We import our empty db and write our model changes to it.

check password setting below!!
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean
from flask.ext.login import UserMixin
from config_vars import MAX_COL_WIDTHS

# ==============================
# DATABASE STRUCTURE
# ==============================
class Member(UserMixin, db.Model):
    'Simple member / user definition'
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(MAX_COL_WIDTHS), nullable=False)
    surname = Column(String(MAX_COL_WIDTHS), nullable=False, unique=True)
    email = Column(String(MAX_COL_WIDTHS), nullable=False, unique=True)
    pwdhash = Column(String, nullable=False)
    adminr = Column(Boolean)

    def __init__(self, firstname, surname, email, password, adminr):
        self.firstname = firstname.title()
        self.surname = surname.title()
        self.email = email.lower()
        self.set_password(password)
        self.adminr = adminr

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return '<{0} {1}>'.format(self.firstname, self.surname)


@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))


if __name__ == '__main__':
    mem = Member('pat','brok','PB','fish', 0)
    print mem
    print mem.pwdhash
    print mem.check_password('Fish'), mem.check_password('fish')
