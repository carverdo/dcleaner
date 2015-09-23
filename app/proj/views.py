"""
With blueprints we can create a second area for view production because
views is independent of 'app'; when app is created it binds to the views.

Use this area to build out the particular project.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import proj
from flask import render_template, current_app, flash, redirect, url_for,  request, session
from ..log_auth.views import login_confirmed
from forms import TimerForm, Form
from ..templates.flash_msg import *
####
from app.gunner import SendEmail2
import ast
from flask.ext.login import current_user


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
        args = ast.literal_eval(form.args.data)
        args = list(args)
        args.append(current_user.firstname)
        args.append(current_user.generate_confirm_token)
        args = tuple(args)
        SendEmail2(*args)
        """
        form.run_task()
        if not form.run_taskFail:
            return redirect(url_for('.curtasks'))
        flash(f60)
        """
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

#from timer_functions import Timo

@proj.route('/screentasks')  ################
def screentasks():
    # fil = open('pare.txt')
    # flash(session.get('object'))
    try: flash(Timo.res)
    except: pass
    return render_template('dummy.html')

@proj.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('testing.html', form=Form())