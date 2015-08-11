"""

"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask.ext.wtf import Form  # Seems odd (this line not next) but wtf Form is slightly different
from wtforms import TextField, StringField, PasswordField, SubmitField, validators
from app.db_models import db, Member
from flask import flash
from config_vars import MAX_COL_WIDTHS, MIN_PASS_LEN

# ==========================
# LOGINS
# ==========================
class SignupForm(Form):
    firstname = StringField("First name",
                           [validators.length(min=1, max=MAX_COL_WIDTHS, message='First name too short/long.')])
    surname = StringField("Surname",
                        [validators.length(min=2, max=MAX_COL_WIDTHS, message='Surname too short/long.')])
    email = StringField("Email",
                        [validators.Email("Please enter a valid email address."),
                         validators.length(max=MAX_COL_WIDTHS, message='email too long.')
                       ])
    password = PasswordField('Password',
                             [validators.length(min=MIN_PASS_LEN, message='4 characters needed in password.')])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        if db.session.query(Member).filter_by(surname=self.surname.data).first():
            self.surname.errors.append("That surname is already taken")
            return False
        if db.session.query(Member).filter_by(email=self.email.data).first():
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    email = StringField("Email",
                        [validators.Email("Please enter a valid email address."),
                         validators.length(max=MAX_COL_WIDTHS, message='email too long.')
                       ])
    password = PasswordField('Password',
                             [validators.length(min=MIN_PASS_LEN, message='4 characters needed in password.')])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        member = db.session.query(Member).filter_by(email=self.email.data).first()
        if member and member.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Ops. Either you need to signUp "
                                     "or that's an invalid e-mail password combo -")
            return False
