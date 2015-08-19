"""

"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask.ext.wtf import Form  # Seems odd (this line not next) but correct: wtf Form is slightly different
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from config_vars import MAX_COL_WIDTHS, MIN_PASS_LEN
from ..db_models import Member


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
                             [validators.length(min=MIN_PASS_LEN, message='4 characters needed in password.'),
                              validators.EqualTo('password2', message='Your passwords must match')
                              ])
    password2 = PasswordField('Confirm Password', [validators.InputRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        if Member.query.filter_by(surname=self.surname.data).first():
            self.surname.errors.append("That surname is already taken")
            return False
        if Member.query.filter_by(email=self.email.data).first():
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True

    def create_newuser(self, form):
        return Member(firstname=form.firstname.data, surname=form.surname.data,
                      email=form.email.data, password=form.password.data)


class SigninForm(Form):
    email = StringField("Email",
                        [validators.Email("Please enter a valid email address."),
                         validators.length(max=MAX_COL_WIDTHS, message='email too long.')
                       ])
    password = PasswordField('Password',
                             [validators.length(min=MIN_PASS_LEN, message='4 characters needed in password.')])
    remember = BooleanField('Remember me?')
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        member = Member.query.filter_by(email=self.email.data).first()
        if member and member.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Oops. Either you need to signUp "
                                     "or that's an invalid e-mail password combo.")
            return False