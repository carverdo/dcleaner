"""
Kept separate as Imports into forms and db_models.
"""
__author__ = 'donal'
__project__ = 'dcleaner'
#todo do we need geography ip addresses?
import os
import re

# ====================
# POPULATE POSTGRES_KEYS AND #1-3 BLANKS AS REQUIRED
# ====================
PK = os.environ.get('POSTGRES_KEYS', 'BLANK BLANK').split()
DBNAME = 'dcleaner'

# ====================
# links db_models.py and forms.py
# ====================
MAX_COL_WIDTHS = 30
MIN_PASS_LEN = 6
ADMIN_USER = False
INITIALLY_ACTIVE = True
LOGOUT = 'Devel_logs.log'

# ====================
# GEOGRAPHY
# ====================
GEO_URL_0 = "http://freegeoip.net/json/{}"
GEO_URL ='http://www.geoplugin.net/json.gp?ip={}'
VALID_IP = re.compile(r"""
\b
(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)
\b
""", re.VERBOSE)

# ====================
# MAILGUN VARIABLES
# ====================
MAILGUN_URL = 'https://api.mailgun.net/v3/{}/messages'
SANDBOX = 'sandbox26a6aabbd3e946feba81293c4b4d9dcc.mailgun.org'
MAILGUN_KEY = os.environ.get('MAILGUN_KEY')

# ====================
# AWS VARIABLES
# ====================
AWS_KEYS = os.environ.get('AWS_KEYS')
if AWS_KEYS is not None:
    tmp = AWS_KEYS.split(' ')
else: tmp = [None, None]
AWS_KEYS = {
    'S3_KEY': tmp[0],
    'S3_SECRET': tmp[1]
    }

# ========================
if __name__ == '__main__':
    print PK
    print AWS_KEYS
