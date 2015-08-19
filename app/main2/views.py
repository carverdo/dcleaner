"""
With blueprints we can create a second area for view production because
views is independent of 'app'; when app is created it binds to the views.

Use this area to build out the particular project.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import main2
from flask import render_template
from flask.ext.login import login_required


# ========================
# Simple Page
# ========================
@main2.route('/')
@main2.route('/home2')
@login_required
def home2():
    return render_template('dummy.html')
