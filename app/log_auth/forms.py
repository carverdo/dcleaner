"""

"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask.ext.wtf import Form  # Seems odd (this line not next) but correct: wtf Form is slightly different
from wtforms import StringField, PasswordField, BooleanField, \
    SelectField, validators, IntegerField
from config_vars import MAX_COL_WIDTHS, MIN_PASS_LEN
from ..db_models import Member, Visit
from pass_stren import PasswordCalc
pc = PasswordCalc()
from flask import flash
from ..templates. flash_msg import *


# ==========================
# LOGINS
# ==========================
class SignupForm(Form):
    firstname = StringField(
            "First name",
            [validators.length(min=1, max=MAX_COL_WIDTHS,
                               message='First name too short/long.')]
    )
    surname = StringField(
            "Surname",
            [validators.length(min=2, max=MAX_COL_WIDTHS,
                               message='Surname too short/long.')]
    )
    email = StringField(
            "Email",
            [validators.Email("Please enter a valid email address."),
             validators.length(max=MAX_COL_WIDTHS, message='email too long.')]
    )
    password = PasswordField(
            'Password',
            [validators.length(
                    min=MIN_PASS_LEN,
                    message='{} characters needed in password.'.format(MIN_PASS_LEN)),
             validators.EqualTo('password2',
                                message='Your passwords must match')]
    )
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
        if pc.get_entropy(self.password.data) == 'weak':
            # self.password.errors.append("That password is too simple")
            flash(f15)
            return True
        else:
            return True


class SigninForm(Form):
    email = StringField(
            "Email",
            [validators.Email("Please enter a valid email address."),
             validators.length(max=MAX_COL_WIDTHS, message='email too long.')]
    )
    password = PasswordField(
            'Password',
            [validators.length(
                    min=MIN_PASS_LEN,
                    message='{} characters needed in password.'.format(MIN_PASS_LEN))]
    )
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
            self.email.errors.append(
                "Oops. Either you need to signUp "
                "or that's an invalid e-mail password combo.")
            return False


class ChangePass(Form):
    email = StringField(
        "Email",
        [validators.Email("Please enter a valid email address."),
         validators.length(max=MAX_COL_WIDTHS, message='email too long.')]
    )
    old_password = PasswordField(
            'old_Password',
            [validators.length(
                    min=MIN_PASS_LEN,
                    message='{} characters needed in password.'.format(MIN_PASS_LEN))]
    )
    new_password = PasswordField(
        'new_Password',
        [validators.length(
            min=MIN_PASS_LEN,
            message='{} characters needed in password.'.format(MIN_PASS_LEN)),
         validators.EqualTo(
                 'new_password2', message='Your passwords must match')]
    )
    new_password2 = PasswordField(
            'Confirm new_Password',
            [validators.InputRequired()]
    )
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
                self.old_password.errors.append(
                    "You cannot change your password until your login"
                    "has been Activated.")
        else:
            self.email.errors.append(
                    "Oops. Either you need to signUp "
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
    adminr = SelectField(
            'Admin',
            choices=[('True', 'Admin'), ('False', 'NotAdmin')]
    )
    active = SelectField(
            'Active',
            choices=[('True', 'Active'), ('False', 'NotActive')],
            default='False',
    )
    confirmed = SelectField(
            'Confirmed',
            choices=[('True', 'Confirmed'), ('False', 'NotConfirmed')],
            default='',
    )
    markfordeletion = SelectField(
            'MFD',
            choices=[(True, 'DELETE'), (False, '')],
            default='',
    )

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


class adminVisits(Form):
    """

    """
    id = IntegerField()
    num_visits = StringField("# Visits")
    num_ips = StringField("# IPs")
    lastdate = StringField("Last Visit")

    def get_existing_data(self, member_id):
        # user-entry data
        memvis = Visit.query.filter_by(member_id=member_id).order_by(Visit.date)
        self.id.default = member_id
        self.num_visits.default = memvis.count()
        self.num_ips.default = len(set([m.ip_address for m in memvis]))  # len(set(memvis.with_entities('ip_address')))
        self.lastdate.default = memvis[-1].date
        # process those changes
        self.process()


# ==========================
# USED?
# ==========================
class SMSForm(Form):
    number = StringField("Number")
