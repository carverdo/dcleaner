"""
Similar to views.py (imported by app and therefore important).
Broken out from views.py to stop that file getting too long.

Handles only the errors.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask import render_template
from . import log_auth


# ========================
# ERRORS
# ========================
@log_auth.app_errorhandler(400)
def page_not_found(e):
    return render_template('error_codes.html',
                           msg='Bad request: integrity error'
                           ), 400


@log_auth.app_errorhandler(404)
def page_not_found(e):
    return render_template('error_codes.html',
                           msg='Page not found'
                           ), 404


@log_auth.app_errorhandler(500)
def page_not_found(e):
    return render_template('error_codes.html',
                           msg='An error: unhandled exception'
                           ), 500
