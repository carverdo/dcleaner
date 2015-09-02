"""
This module is a template and explains as it goes down the page.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask import render_template, redirect, url_for, flash, \
    current_app, request, abort
from forms import SignupForm, SigninForm, ChangePass
from flask.ext.login import login_user, logout_user, \
    login_required, current_user
from datetime import datetime
from . import log_auth
from ..templates.flash_msg import *
from ..db_models import Member, Visit
## from .. import cache
# from .. import lg  # don't auto-delete: see below
from geodata import get_geodata, _key_modifier
from ..gunner import send_email
from functools import wraps
from urlparse import urlparse, urljoin

# ========================
# HELPER FUNCTIONS
# ========================
# @cache.cached(timeout=20)  # NO GOOD FOR THE FLASHES!
def set_template(template, form, fn, patex, tadata):
    return render_template(template, form=form, fn=fn,
                           patex=patex, tadata=tadata)


def redirect_already_authenticateds(current_user):
    if current_user.is_authenticated():
        flash(f120)
        return resolve_confirm_status(current_user)
    else: return None


def process_forms_and_redir(form):
    """
    Only if form validates will it do anything,
    signing up new members or signing in old ones,
    and returning the redirect endpoint.
    """
    if form.validate_on_submit():
        member = Member.query.filter_by(email=form.email.data).first()
        # New members signing up
        if member is None:
            newuser = Member.create(**form.data)
            login_user(newuser)
            token = newuser.generate_confirm_token()
            send_email(newuser.email, 'Activate your Signin', 'confirm_body',
                       newuser=newuser, token=token)
            flash(f20 + ' ' + f21)
            return '.home'
        # Existing (/active) members
        else:
            login_user(member, remember=form.remember.data)
            return resolve_confirm_status(current_user)


def resolve_confirm_status(current_user, token=None):
    if current_user.confirmed or current_user.confirm_token(token):
        current_user.ping()
        flash(f30)
        # Visit.create(**get_geodata())
        return 'proj.home2'
    else:
        if token: flash(f130 + ' ' + f131)
        else: flash(f130)
        return '.home'


def login_confirmed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous() or not current_user.confirmed:
            return redirect(url_for('log_auth.signin'))
        return f(*args, **kwargs)
    return decorated_function


# ========================
# UNUSED FUNCTIONS
# ========================
def get_redirect_target():
    """
    Redirects can now SAFELY incorporate the request.arg 'next':
    ie a previous redirect to ourPage included url_for('ourPage', next='SOME PAGE'),
    any redirect on ourPage would now read:
    redirect(g_r_t() or url_for(blah blah))
    since we know g_r_t() only produces safe urls
    and here g_r_t() will reproduce 'SOME PAGE' as a result.

    :return: valid targets only
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if _url_is_valid(target):
            return target
        else:
            abort(400)

def _url_is_valid(target):
    """
    :param target: potentially dangerous url
    :return: True if safe
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# ========================
# STATIC PAGES
# ========================
@log_auth.route('/')
@log_auth.route('/home')
# @cache.cached(timeout=20)
def home():
    # current_app.logger.info('On screen words 1')
    # lg.logger.info('Text words 1')
    Visit.create(**get_geodata(True, _key_modifier))
    return render_template('home.html', ct=datetime.utcnow())


@log_auth.route('/contactus')
## @cache.cached(timeout=200)
def contactus():
    return render_template('contactus.html')


@log_auth.route('/signout')
@login_required
## @cache.cached(timeout=200)
def signout():
    logout_user()
    return redirect(url_for('.home'))


# ========================
# SIGNUP
# There is always going to be some sort of sign-up.
# We have master_panels which are fed headers via patex
# and whose contents are fed by templates via tadata
# ========================
@log_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    redir = redirect_already_authenticateds(current_user)
    if redir: return redirect(url_for(redir))
    redir = process_forms_and_redir(form)
    if redir:
        return redirect(url_for(redir))
    else:
        return set_template('signing.html', form, '.signup',
                            current_app.config['PAHDS']['signup'],
                            current_app.config['TADATA']['signup']
                            )


@log_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    redir = redirect_already_authenticateds(current_user)
    if redir: return redirect(url_for(redir))
    redir = process_forms_and_redir(form)
    if redir:
        return redirect(url_for(redir))
    else:
        return set_template('signing.html', form, '.signin',
                            current_app.config['PAHDS']['signin'],
                            current_app.config['TADATA']['signin']
                            )

# ========================
# ACTIVATION TOKEN HANDLING
# 1. first layer security: login_required
# ========================
@log_auth.route('/confirm/<token>')
@login_required
def confirm(token):
    return redirect(url_for(
        resolve_confirm_status(current_user, token=token)))


@log_auth.route('/confirm')
@login_required
def resend_token():
    token = current_user.generate_confirm_token()
    send_email(current_user.email, 'Activate your Signin', 'confirm_body',
               newuser=current_user, token=token)
    flash(f21)
    return redirect(url_for('.home'))


# ========================
# PROFILE
# currently just allows change of password
# 2. second layer: login_confirmed
# ========================
@log_auth.route('/profile', methods=['GET', 'POST'])
@login_confirmed
def profile():
    form = ChangePass()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        current_user.save()
        return redirect(url_for(
            resolve_confirm_status(current_user)
        ))
    return set_template('signing.html', form, '.profile',
                        current_app.config['PAHDS']['profile'],
                        current_app.config['TADATA']['profile']
                        )


# ========================
# UNDER TESTING
# just tinkering with formatting; not quite right
# ========================
@log_auth.route('/sendsms')
@login_required
def sendsms():
    # token = current_user.generate_confirm_token()
    token, SMS = ' TEST TOKEN ', '+4478[8 DIGITS no spaces]@mmail.co.uk'
    send_email(SMS, 'Activate your Signin', 'confirm_bodySMS',
               newuser=current_user, token=token)
    return redirect(url_for('.home'))