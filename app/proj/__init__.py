"""
Be careful with circularity.
"""
__author__ = 'donal'
__project__ = 'dcleaner'

# to be used in views -
from flask import Blueprint
proj = Blueprint('proj', __name__)
# same, and for relative addressing -
# from intake_raw import DataHandler
from data_handler2 import DataHandler2
# from xx_type_stamp import TypeStamper
from se_corrects import FromStrTo
fst = FromStrTo()

# needs to go last (coming back from views) -
from . import views