__author__ = 'donal'
__project__ = 'dataHoover'
import os
# todo Ugly ugly DL_DIR bodge

# ============
# LOGGING VARIABLES
# ============
# Meta Data
VERSION = "1.0"
PROJECT_NAME = 'IFAprovPat'
# S3 Bucket
EXCEL_BASE_DIR = 'dataclean'
# Downloads dir
DL_DIR = "C:\\MagicFolder"  # os.path.join(os.path.expanduser('~'), 'downloads')
# Starting letter in name of excel file to be used once in the Downloads dir
EXCEL_SOURCE = "RawData"
EXCEL_SUFFIX = '.xls'
EXCEL_ALLOWABLE_TYPES = ['empty', 'text', 'number',
                         'xldate', 'boolean', 'error']  # ordering matters!

# ============
# BASIC html5 FORM DEFAULTS
# ============
# name, id
f_empty = {'type': "search", 'name': "f_empty ", 'css': "lightgray"}  # 'value': "NULL ENTRY",
f_text = {'type': "search", 'name': "f_text ", 'css': "teal"}
f_number = {'type': "number", 'name': "f_number ", 'step': 'any', 'css': "mediumblue"}  # "lightcyan"}
f_date = {'type': "datetime", 'name': "f_date ", 'css': "darkorange"}  # deepskyblue
f_bool = {'type': "number", 'name': "f_bool ", 'min': -1, 'max': 1, 'step': 1, 'css': "cornflowerblue"}
f_error = {'type': "search", 'name': "f_error ", 'css': "lightgray", 'value': "ERROR"}
f_query = {'type': "search", 'name': "f_query "}

# ============
# MAP FROM LABELS (AUTO-GENERATED) TO html5 FORMS
# ============
FORM_DICT_VARS = {
    'empty': f_empty,
    'text': f_text,
    'number': f_number,
    'xldate': f_date,
    'boolean': f_bool,
    'error': f_error
}

"""
FORM_DICT = dict(zip(EXCEL_ALLOWABLE_TYPES,
                     ['f_empty', 'f_text', 'f_number',
                      'f_date', 'f_bool', 'f_error']))
"""
# USER = 'Explo_UserName'
# AWS_BASE_DIR = 'circadianboard'