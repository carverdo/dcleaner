__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from flask import Blueprint
devy = Blueprint('device', __name__)
from . import views
