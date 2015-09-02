"""
With blueprints we can create a second area for view production because
views is independent of 'app'; when app is created it binds to the views.

Use this area to build out the particular project.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import proj
from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user

from ..log_auth.views import login_confirmed
# ========================
# Simple Page
# ========================
@proj.route('/')
@proj.route('/home2')
@login_confirmed
def home2():
    """
    if current_user.confirmed:
        return render_template('dummy.html')
    return redirect(url_for('main.home'))
    """
    return render_template('dummy.html')