__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, view_errors
