"""
With blueprints we can create a second area for view production because
views is independent of 'app'; when app is created it binds to the views.

Use this area to build out the particular project.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import proj
from flask import render_template, current_app, flash, redirect, url_for,  request
from ..log_auth.views import login_confirmed
from forms import TimerForm
from ..templates.flash_msg import *


# ========================
# Simple Page
# ========================
@proj.route('/')
@proj.route('/home2')
@login_confirmed
def home2():
    return render_template('dummy.html')


@proj.route('/addtasks', methods=['GET', 'POST'])
@login_confirmed
def addtasks():
    form = TimerForm()
    if form.validate_on_submit():
        form.run_task()
        if not form.run_taskFail:
            return redirect(url_for('.curtasks'))
        flash(f60)
    else:
        form.get_args()
        form.update_vals()
    return render_template('signing.html', form=form, fn='.addtasks',
                           patex=current_app.config['PAHDS']['addtasks'],
                           tadata=current_app.config['TADATA']['addtasks'],
                           wid=4
                           )


@proj.route('/curtasks', methods=['GET', 'POST'])
@login_confirmed
def curtasks():
    form = TimerForm()
    if request.method == 'POST':
        form.remove_group(request.values['btn'])
    return render_template('signing.html', form=form, fn='.curtasks',
                           patex=current_app.config['PAHDS']['curtasks'],
                           tadata=current_app.config['TADATA']['curtasks'],
                           wid=8
                           )
