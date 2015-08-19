"""
This module is a template and explains as it goes down the page.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask import render_template, redirect, url_for, flash, current_app
from forms import SignupForm, SigninForm
from flask.ext.login import login_user, logout_user, login_required, current_user
from datetime import datetime
from . import main
from ..templates.flash_msg import *
from .. import db
from ..db_models import Member
from .. import cache
from .. import lg  # don't auto-delete: see below


# ========================
# HELPER FUNCTIONS
# ========================
# @cache.cached(timeout=20)  # NO GOOD FOR THE FLASHES!
def set_template(template, form, fn, patex, tadata):
    return render_template(template, form=form, fn=fn,
                           patex=patex, tadata=tadata)


def redirect_already_authenticateds(current_user):
    if current_user.is_authenticated():
        flash(f1)
        return '.home'
    else: return None


def process_forms_and_redir(form):
    """
    Only if form validates will it do anything,
    signing up new members or signing in old ones,
    and returning the redirect endpoint.
    """
    if form.validate_on_submit():
        member = Member.query.filter_by(email=form.email.data).first()
        # existing (/active) members
        if member is not None:
            if login_user(member, remember=form.remember.data):
                current_user.ping()
                flash(f3)
            else: flash(f4)
            return 'main2.home2'
        # new members signing up
        elif 'password2' in form.__dict__.keys():
            newuser = form.create_newuser(form)
            db.session.add(newuser)
            db.session.commit()
            login_user(newuser)
            return 'main2.home2'


# ========================
# Simple HomePage & Contacts
# ========================
@main.route('/')
@main.route('/home')
# @cache.cached(timeout=20)
def home():
    # current_app.logger.info('On screen words 1')
    # lg.logger.info('Text words 1')
    return render_template('home.html', ct=datetime.utcnow())


@main.route('/contactus')
@cache.cached(timeout=200)
def contactus():
    return render_template('contactus.html')


# ========================
# SIGNUP
# There is always going to be some sort of sign-up.
# We have master_panels which are fed headers via patex
# and whose contents are fed by templates via tadata
# ========================
@main.route('/signup', methods=['GET', 'POST'])
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


@main.route('/signin', methods=['GET', 'POST'])
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


@main.route('/signout')
@login_required
## @cache.cached(timeout=200)
def signout():
    logout_user()
    return redirect(url_for('.home'))
