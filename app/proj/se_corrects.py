__author__ = 'donal'
__project__ = 'dataHoover'

from dateutil import parser
import re
# To catch '..', '-' etc as nulls -
NOT_NULLS = re.compile(r'[a-zA-Z0-9]')
NULL_LEN_MAX = 2
# To catch '25APR2012 | 25APR12 | 25APR | 25APR2012T13:57PM' as date -
DATE_PATT = re.compile(r'\d{1,2}[a-zA-Z]{3,4}(\d{4}|\d{2}|)')  # \B
DATE_REPLACE_BOUNDARY = re.compile('\d[a-zA-Z]')
# To only catch '25042012' (ascending) or '20120425' (descending) -
EIGHT_PATT = re.compile(r'\d{8}')
# To widen bools -
BOOL_TRUE_LIKES = ['t', 'true', '1']
BOOL_FALSE_LIKES = ['f', 'false', '0']
BOOL_UNKNOWNS = ['unk', 'unknown']
# No future dates -
from datetime import datetime

class FromStrTo(object):
    """
    Handles cases where we have a string (our 'raw') and want
    to convert it to something else.
    The init has been set up so that we can also later call it again
    from run_parse.

    NOTE: the operative functions 'to_empty' etc. have been named so that the
    word after 'to_' is an excel label.
    This is used in pack_it_up: convert_instruction = 'to_{}'.format(required)
    """
    def __init__(self, raw=None, method=None):
        self.cutoff = datetime.today()
        self.raw, self.sec = None, None
        if isinstance(raw, str) or isinstance(raw, unicode):
            self.raw = raw.strip()
        if self.raw and method: getattr(self, method)()

    def run_parse(self, method, raw=None):
        self.__init__(raw, method)

    def to_number(self):
        print self.raw.replace('.', '').isdigit()
        if self.raw.replace('.', '').isdigit():
            try: self.sec = float(self.raw)
            except: pass

    def to_xldate(self):
        try:
            tmp = parser.parse(self.raw)
            if tmp.hour==0 and tmp.minute==0: oput = '%Y-%m-%d'
            else: oput = '%Y-%m-%d %H:%M'
            self.sec = tmp.strftime(oput)
        except:
            self._run_parser_with_modified_string()

    def _run_parser_with_modified_string(self):
        if re.match(DATE_PATT, self.raw):  # dates
            pos = re.search(DATE_REPLACE_BOUNDARY, self.raw).start() + 1
            refo = self.raw[:pos] + ' ' + self.raw[pos:]
        elif re.match(EIGHT_PATT, self.raw):  # eights
            refo = self.raw[-4:] + self.raw[2:4] + self.raw[:2]
        try:  # ie not all patterns will work
            refo = parser.parse(refo)
            if refo < self.cutoff:
                if refo.hour == 0 and refo.minute == 0: oput = '%Y-%m-%d'
                else: oput = '%Y-%m-%d %H:%M'
                self.sec = refo.strftime(oput)
        except: pass

    def to_boolean(self):
        if self.raw.lower() in BOOL_TRUE_LIKES: self.sec = 1
        elif self.raw.lower() in BOOL_FALSE_LIKES: self.sec = 0
        elif self.raw.lower() in BOOL_UNKNOWNS: self.sec = -1

    def to_empty(self):
        if (len(self.raw) <= NULL_LEN_MAX and
            not re.match(NOT_NULLS, self.raw)): self.sec = 'NULL ENTRY'

# =============
# YEARS ONLY
# ============
years_only = [
    '2008'  # assumes prevailing dayMo
]
# =============
# YEARMOS
# ============
yearmos = [
    'Jun 2010',  # dont care about (no)spaces, dashes
    'June-2010',
    'AUG2008',  # or uppercase, titlecase
    'aug2008',
    'Sep2010',  # dont care about 3 or 4 letters
    'Sept2010',
    'sep08',  # or 2 digits
    'sep-08',
    '2007-june',  # or yearMo vs moYear
    '2007 jun',
    '2007 june',
    '2007 Jun',
    '2007 June',
    '2007 04',  # or digit-mos
    '2007 4'
]
# =============
# YEARMODAYS
# ============
yearmodays = [
    '28-11-12',  # 2/4 digits, dash no dash
    '28-11-2012',
    '28 11 2012',
    '1APR10',  # ADJUSTED: NEEDS A SPACE
    '30Sept10',
    '15-Feb-2013',  # wordmos
    '15 Feb 2013',
    '2005 Jun 1',  # reverse order
    'Mar 1 2005',  # american
    '2005 6 1',  # missing lead-zeroes
    '2005 6 01'
]
# =============
# MODAYS
# ============
modays = [
    '25-APR',  # will default to this year
    '25-apr',
    'apr 25',
    '04 25'
]

# =============
# EIGHTS
# ============
eights = [
    '01112014',  # should work (ascending) but doesn't
    '20141101',  # descending
    '13042914',  # just a long way away off
    '32012014',  # bad day, mo, yr
    '02132014',  #
    '04201401',  # year-middle
    '01012014a',  # not an eight
    'a01012014'  #
]

# =============
# DATETIME
# ============
datims = [
    'Jun 1 2005  1:33PM',
    'Jun 1 2005  1333',
    '1 Jun 05  1333',
    'Jun 1 05 13:33',
    'Jun 1 2005T1:33PM',
    '25 Jun 2005T1:33PM',
    '25 JUN 2005T1:33PM',
    '25 JUNE 2005T1:33PM',
    '25Jun2005T1:33PM',
]

# =============
# NOT WHAT YOU THINK
# the module fills left (got one? its date; got two? its mo date)
# ============
nwyt = [
    '09',  # assumes date in current moYr (VS 2009)
    '07 4',  # ERROR? assumes moDa of current year (VS 2007 4)
    '25 04',  # FAILS: assumes its moDa
]


if __name__ == '__main__':
    print '=============NULLS============'
    print 'should adjust -'
    for ele in ['-', '--', '/']:
        fst = FromStrTo(ele, 'to_empty')
        print fst.sec
    print 'should be none -'
    for ele in ['a', 'b', 'n/a']:
        fst = FromStrTo(ele, 'to_empty')
        print fst.sec
    print 'WEIRD -'
    fst = FromStrTo('------------', 'to_xldate')
    print fst.sec
    print '=============BOOLS============'
    print 'adjusts - '
    for ele in ['t', 'True', 'false', '1']:
        fst = FromStrTo(ele, 'to_boolean')
        print fst.sec
    print 'non-adjusts - '
    for ele in ['tru', 'fals', 0, 1]:
        fst = FromStrTo(ele, 'to_boolean')
        print fst.sec
    print '=============NUMS============'
    print 'adjusts - '
    for ele in ['1', '265', '2222223445']:
        fst = FromStrTo(ele, 'to_number')
        print fst.sec
    print 'non-adjusts - '
    for ele in ['A1', '265mg', '222 2223445']:
        fst = FromStrTo(ele, 'to_number')
        print fst.sec

    print '=============DATES============'
    for ele in years_only:
        fst = FromStrTo(ele, 'to_xldate')
        print fst.sec
    print '-'
    for ele in yearmos:
        fst = FromStrTo(ele, 'to_xldate')
        print fst.sec
    print '-'
    for ele in yearmodays:
        fst = FromStrTo(ele, 'to_xldate')
        print fst.sec
    print '-'
    for ele in modays:
        fst = FromStrTo(ele, 'to_xldate')
        print fst.sec
    print '-'
    print 'only the first two will work (third is too far in future)'
    for ele in eights:
        fst = FromStrTo(ele, 'to_xldate')
        print fst.sec
    print '-'
    for ele in datims:
        fst = FromStrTo(ele, 'to_xldate')
        print fst.sec

    print '=============NOT WHAT YOU THINKS============'
    for ele in nwyt:
        fst = FromStrTo(ele, 'to_xldate')
        print fst.sec
