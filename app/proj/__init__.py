__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from flask import Blueprint
proj = Blueprint('proj', __name__)
from . import views
