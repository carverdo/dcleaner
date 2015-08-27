"""
With blueprints we can create a second area for view production because
views is independent of 'app'; when app is created it binds to the views.

Use this area to build out the particular project.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import main2
from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user


# ========================
# Simple Page
# ========================
@main2.route('/')
@main2.route('/home2')
@login_required
def home2():
    if current_user.confirmed:
        return render_template('dummy.html')
    return redirect(url_for('main.home'))