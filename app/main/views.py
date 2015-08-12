"""
This module is a template and explains as it goes down the page.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask import render_template, redirect, url_for, flash
from forms import SignupForm, SigninForm
from app import app, db, lg
from app.templates.flash_msg import *
from app.db_models import Member
from flask.ext.login import login_user, logout_user, login_required, current_user, login_fresh
from datetime import datetime


# ========================
# Simple Home Page
# ========================
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', ct=datetime.now())


# ========================
# SIGNUP
# There is always going to be some sort of sign-up.
# We have master_panels which are fed headers via patex
# and whose contents are fed by templates via tadata
# ========================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if current_user.is_authenticated():
        current_user.ping()
        flash(f1)
        return redirect(url_for('home'))
    if form.validate_on_submit():
        # Database operations [ENTER YOUR OWN]
        newuser = form.create_newuser(form, app.config['ADMIN_USER'])
        db.session.add(newuser)
        db.session.commit()
        login_user(newuser)
        flash(f2)
        return redirect(url_for('home'))
    return render_template(
        'signing.html', form=form, fn='signup',
        patex=app.config['PAHDS']['signup'],
        tadata=app.config['TADATA']['signup']
    )


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if current_user.is_authenticated():
        current_user.ping()
        flash(f1)
        return redirect(url_for('home'))
    if form.validate_on_submit():
        member = db.session.query(Member).filter_by(email=form.email.data).first()
        if member is not None:
            login_user(member, remember=form.remember.data)
            # member.ping()
            current_user.ping()
            flash(f3)
            return redirect(url_for('home'))  # profile for graph
    return render_template(
        'signing.html', form=form, fn='signin',
        patex=app.config['PAHDS']['signin'],
        tadata=app.config['TADATA']['signin']
    )


@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('home'))
