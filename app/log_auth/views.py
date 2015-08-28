"""
This module is a template and explains as it goes down the page.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask import render_template, redirect, url_for, flash, current_app
from forms import SignupForm, SigninForm, ChangePass
from flask.ext.login import login_user, logout_user, login_required, current_user
from datetime import datetime
from . import log_auth
from ..templates.flash_msg import *
from ..db_models import Member, Visit
## from .. import cache
# from .. import lg  # don't auto-delete: see below
from geodata import get_geodata, _key_modifier
from ..gunner import send_email


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


# ========================
# STATIC PAGES
# ========================
@log_auth.route('/')
@log_auth.route('/home')
# @cache.cached(timeout=20)
def home():
    # current_app.logger.info('On screen words 1')
    # lg.logger.info('Text words 1')
    """
    flash(str(get_geodata(True, _key_modifier)))
    res = get_geodata(True, _key_modifier)
    res['longitude'], res['latitude'] = 10, 10
    res['member_id'] = 1
    ##Visit.create(**get_geodata(True, _key_modifier))
    flash(str(res))
    v = Visit(**res)
    flash(str(v))

    db.session.add(v)
    db.session.commit()
    # Visit.create(**res)
    """
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
# ========================
@log_auth.route('/profile', methods=['GET', 'POST'])
@login_required
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
