"""

"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask.ext.wtf import Form  # Seems odd (this line not next) but correct: wtf Form is slightly different
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    SelectField, validators, IntegerField
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
                             [validators.length(min=MIN_PASS_LEN,
                                                message='{} characters needed in password.'.format(MIN_PASS_LEN)
                                                ),
                              validators.EqualTo('password2', message='Your passwords must match')
                              ])
    password2 = PasswordField('Confirm Password', [validators.InputRequired()])
    # submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        if Member.query.filter_by(email=self.email.data).first():
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
                             [validators.length(min=MIN_PASS_LEN,
                                                message='{} characters needed in password.'.format(MIN_PASS_LEN))
                              ])
    remember = BooleanField('Remember me?')
    # submit = SubmitField("Sign In")

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


class ChangePass(Form):
    email = StringField("Email",
                        [validators.Email("Please enter a valid email address."),
                         validators.length(max=MAX_COL_WIDTHS, message='email too long.')
                       ])
    old_password = PasswordField('old_Password',
                             [validators.length(min=MIN_PASS_LEN,
                                                message='{} characters needed in password.'.format(MIN_PASS_LEN))
                              ])
    new_password = PasswordField('new_Password',
                             [validators.length(min=MIN_PASS_LEN,
                                                message='{} characters needed in password.'.format(MIN_PASS_LEN)
                                                ),
                              validators.EqualTo('new_password2', message='Your passwords must match')
                              ])
    new_password2 = PasswordField('Confirm new_Password', [validators.InputRequired()])
    # submit = SubmitField("Change Password")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        member = Member.query.filter_by(email=self.email.data).first()
        if member and member.check_password(self.old_password.data):
            if member.confirmed:
                return True
            else:
                self.old_password.errors.append("You cannot change your password until your login"
                                                "has been Activated.")
        else:
            self.email.errors.append("Oops. Either you need to signUp "
                                     "or that's an invalid e-mail password combo.")
            return False


# ==========================
# ADMINISTRATOR EDITING PLATES
# ==========================
class adminMember(SignupForm):
    """
    Inherit (from signup), modify (including default in model),
    and auto-present the pre-populated forms data.
    """
    id = IntegerField()
    adminr = SelectField('Admin', choices=[('True', 'Admin'), ('False', 'NotAdmin')])
    active = SelectField('Active', choices=[('True', 'Active'), ('False', 'NotActive')], default='False',)
    confirmed = SelectField('Confirmed', choices=[('True', 'Confirmed'), ('False', 'NotConfirmed')], default='',)
    markfordeletion = SelectField('MFD', choices=[(True, 'DELETE'), (False, '')], default='',)

    def get_existing_data(self, member):
        # user-entry data
        self.id.default = member.id
        self.firstname.default = member.firstname
        self.surname.default = member.surname
        self.email.default = member.email
        # defaults in model
        self.adminr.default = member.adminr
        self.active.default = member.active
        self.confirmed.default = member.confirmed
        self.markfordeletion.default = False
        # process those changes
        self.process()


class SMSForm(Form):
    number = StringField("Number")