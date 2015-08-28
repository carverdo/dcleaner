"""
We import our empty db and write our model changes to it.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask.ext.login import UserMixin
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config_vars import MAX_COL_WIDTHS, ADMIN_USER, INITIALLY_ACTIVE

# ==============================
# DATABASE STRUCTURE
# ==============================
class CRUDMixin(object):
    """Inherit object for common operations"""
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, commit=True, **kwargs):
        # a bit bespoke (for new signups) -
        kwargs.pop('password2', None)
        kwargs.pop('submit', None)
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # Also proxy Flask-SqlAlchemy's get_or_44 for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class Member(UserMixin, CRUDMixin, db.Model):
    """Simple member / user definition"""
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(MAX_COL_WIDTHS), nullable=False)
    surname = Column(String(MAX_COL_WIDTHS), nullable=False)
    email = Column(String(MAX_COL_WIDTHS), nullable=False, unique=True)
    pwdhash = Column(String, nullable=False)
    adminr = Column(Boolean)
    active = Column(Boolean)
    confirmed = Column(Boolean, default=False)
    first_log = Column(DateTime(), default=datetime.utcnow)
    last_log = Column(DateTime(), default=datetime.utcnow)
    logins = Column(Integer)
    ips = relationship('Visit', backref='member',
                       cascade="all, delete-orphan", passive_deletes=True)

    def __init__(self, firstname, surname, email, password,
                 adminr=ADMIN_USER, active=INITIALLY_ACTIVE,
                 confirmed=False,
                 first_log=datetime.utcnow(), last_log=datetime.utcnow(), logins=1):
        self.firstname = firstname.title()
        self.surname = surname.title()
        self.email = email.lower()
        self.set_password(password)
        self.adminr = adminr
        self.active = active
        self.confirmed = confirmed
        self.first_log = first_log
        self.last_log = last_log
        self.logins = logins

    def set_password(self, password):
        self.pwdhash = generate_password_hash(
            password, method='pbkdf2:sha512:10000')

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    # ===========================
    # Next 4 all for flask-login
    # UserMixin would handle ordinarily, but in case we modify
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
    # ===========================
    def ping(self):
        self.last_log = datetime.utcnow()
        self.logins += 1
        self.save(self)
    # ===========================
    # ACTIVATION
    def generate_confirm_token(self, expiry=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiry)
        return s.dumps({'confirm': self.id})
    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.save(self)
        return True

    def __repr__(self):
        return '<{0} {1}>'.format(self.surname, self.email)


class Visit(CRUDMixin, db.Model):
    __tablename__ = 'visit'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    browser = Column(String)
    city = Column(String)
    zip_code = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(DateTime(), default=datetime.utcnow)
    member_id = Column(Integer, ForeignKey('member.id', ondelete='CASCADE'))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '<Visit for ip {} in {} at {:%Y-%m-%d %H:%M:%S}>'\
            .format(self.ip_address, self.city, self.date)


# flask-login needs this definition
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))


if __name__ == '__main__':
    mem = Member('pat','brok','PB','fish', 0)
    print mem
    print mem.pwdhash
    print mem.check_password('Fish'), mem.check_password('fish')
