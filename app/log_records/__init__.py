__author__ = 'donal'
__project__ = 'dcleaner'

from flask import Blueprint
log_recs = Blueprint('log_recs', __name__)
from . import views