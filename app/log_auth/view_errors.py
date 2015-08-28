"""
Similar to views.py (imported by app and therefore important).
Broken out from views.py to stop that file getting too long.

Handles only the errors.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import log_auth
from flask import render_template


# ========================
# ERRORS
# ========================
@log_auth.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@log_auth.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
