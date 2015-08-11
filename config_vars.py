import os

__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

# ====================
# POPULATE POSTGRES_KEYS AND #1-3 BLANKS AS REQUIRED
# ====================
PK = os.environ.get('POSTGRES_KEYS', 'BLANK BLANK').split()
DBNAME = 'skeleton_1'

# links db_models.py and forms.py
MAX_COL_WIDTHS = 30
MIN_PASS_LEN = 4