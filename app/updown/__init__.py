__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from flask import Blueprint
updo = Blueprint('updown', __name__)
from . import views
