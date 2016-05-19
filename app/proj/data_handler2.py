"""
This variant replaces the original in intake_raw.

I don't much like it because it assumes boto (see how keys are part of
the original init) but we have no choice for now.
"""

import pickle
import string
from functools import wraps
import os
import xlrd
# from app import lg  # don't auto-delete: see below
from config_project import EXCEL_ALLOWABLE_TYPES, EXCEL_SOURCE

# todo xlrd only looks to xls files; need to investigate other readers.
# todo namedTuples simplified things in tiab_processing/parse_exTab
# todo cant delete the original excel file, linked to the try/except loop.

__author__ = 'donal'
__project__ = 'dcleaner'


def build_excel_col_headers(ncols):
    base_ls = list(string.ascii_uppercase)
    multi_ls = [string.ascii_uppercase[idx] + k for idx in
                range(ncols // len(base_ls)) for k in base_ls]
    return (base_ls + multi_ls)[:ncols]
# build_excel_col_headers(tab.ncols)

class DataHandler2(object):
    """
    *** NOTE: the ASSUMPTION that IDs map to allowable_types ***

    Assumes the format of the document will have the top row / leftmost column
    reserved for "hidden/ignore" tags; ie any markings here ensure that the
    corresponding row or column is not read in.

    header_rows is like length, ie the number of rows that acts as spacers
    before you get to raw data; the
    default (2) essentially assumes we have row1 for hidden tags; row2 for the
    actual header.

    label_row is a single column for the column that actually represents
    the header and contains labels we wish to show; the
    default (1) assumes we have not the zeroth(row1) but the first (row2) as
    container for the labels;
    """
    allowable_types = EXCEL_ALLOWABLE_TYPES
    type_codes = dict(enumerate(allowable_types))
    pickle_e_msg = 'WARNING: method <{}> not run. ' \
                   'You need to reload class with use_pickle=False'

    def __init__(self, keys, file_name=EXCEL_SOURCE,
                 header_rows=2, label_row=1,
                 use_pickle=True):
        # classic inits
        self.keys = keys
        self.header_rows,  self.label_row = header_rows, label_row
        self.use_pickle = use_pickle
        # s3 stores of keys and their data
        self.p_summ, self.p_data, self.p_html = None, None, None
        self.tmp_s, self.tmp_d, self.tmp_h = None, None, None
        # local vars
        self.book, self.summary, self.coro_idxs = None, {}, {}
        self.raw_data, self.html_pack = {}, {}
        # will vary by tab (set later)
        self.ig_rows, self.rem_rows, self.ig_cols, self.rem_cols = \
            None, None, None, None
        # ==================
        # FIRST OPERATION
        # snapshot of basic data (only snapshot for now; speed)
        # ==================
        self.key = self.find_key(file_name)
        if self.key:
            self.build_subkeys()
            self.build_summary()

    # =======================================
    # A. AUTORUNS: RUN IF KEY FORMATTED PROPERLY
    # Build summary is very important; with it we can handily store
    # much information without having to access the file again
    # =======================================
    def build_subkeys(self):
        """
        keys: stores of data
        """
        self.p_summ = os.path.splitext(self.key.name)[0] + '_SUMM.p'
        self.p_data = os.path.splitext(self.key.name)[0] + '_DATA.p'
        self.p_html = os.path.splitext(self.key.name)[0] + '_HTML.p'

    def build_summary(self):
        """
        optionally chooses from the pickle of the same name;
        typically the function named as string will run first time only
        """
        self.divert_on_pickle('summary', self.p_summ, '_build_summary')

    def _build_summary(self):
        """
        :return: summary of the worksheets; intake of summary data;
        pickles the object afterwards.
        """
        # first, grab file metadata
        self.summary['meta'] = self.key.etag[1:-1], self.key.last_modified
        # second, build a workbook summary
        self.book = xlrd.open_workbook(file_contents=
                                       self.key.get_contents_as_string())
        self.summary['WorkBook'] = {
            'COLUMNS assumed/HEADER DEPTH': 'x{} ROW'.format(self.header_rows),
            '# tabs': self.book.nsheets,
            'tab names': self.book.sheet_names()
        }
        # third, and most important: summary data per worksheet
        # this is used later to save on data calls
        # especially wrt coro_idxs
        active_tabs = []
        for tab in self.book.sheets():
            if tab.nrows >= self.header_rows:
                tmp  = self.set_ignores(tab.name)
                ## tmp = (list(self.rem_cols), list(self.rem_rows))
                self.summary[tab.name] = {
                    'cols by rows': '{} by {}'.format(*tmp),
                    'column_headers': [tab.cell_value(self.label_row, col_idx)
                                       for col_idx in tmp[0]]
                }
                self.coro_idxs[tab.name] = tmp
                active_tabs.append(tab.name)
            else:
                self.summary[tab.name] = {'cols by rows': 'EMPTY'}
        self.summary['active_tabs'] = active_tabs
        self.tmp_s = pickle.dumps(self.summary, -1)

    # ============================
    # B. HTML OUTPUT
    # part 1 for pickle; part 2 if doing for first time
    # this section is actively called in the view function
    # and typically relates to one tab (ie the tab that has been clicked)
    # ============================
    def package_for_html(self):
        """
        optionally chooses from the pickle of the same name;
        """
        self.divert_on_pickle('raw_data', self.p_data, '_build_raw')
        self.divert_on_pickle('html_pack', self.p_html, '_package_for_html')

    def _package_for_html(self):
        """
        pickles the object afterwards.
        """
        if not self.raw_data:
            self._build_raw()
        for tab_name in self.summary['active_tabs']:
            transpose = map(list, zip(*self.get_ctype_bins(tab_name)))
            data = dict(zip(self.type_codes.values(), transpose))
            rem_cols, rem_rows = self.coro_idxs[tab_name]
            tab = self.book.sheet_by_name(tab_name)
            self.html_pack[tab_name] = {
                'tab': tab_name,
                'headers': zip(
                    [lab for ct, lab in enumerate(self.get_cols(tab.name)) if
                     ct in rem_cols],
                    [tab.cell_value(self.label_row, col_idx) for col_idx in
                     rem_cols]
                ),
                'coro_idxs': (rem_cols, rem_rows),
                'data': data
            }
        self.tmp_h = pickle.dumps(self.html_pack, -1)

    # ============================
    # C. GENERATING RAW DATA
    # part 1 for pickle; part 2 if doing for first time
    # ============================
    def _build_raw(self):
        """
        only builds from sheets where data present.
        pickles the object afterwards.
        """
        for tab in self.book.sheets():
            if tab.nrows >= self.header_rows:
                # self.set_ignores(tab.name)
                self.raw_data[tab.name] = self.absorb_data_columns(tab.name)
            else: pass
        self.tmp_d = pickle.dumps(self.raw_data, -1)

    # ============================
    # XLRD FUNCTIONS
    # These functions access the workbook
    # and so typically will need to use tab = self.book...
    # ============================
    def set_ignores(self, tab_name):
        """determines those rows and cols to ignore on any tab"""
        tab = self.book.sheet_by_name(tab_name)
        ig_cols = set(
            [ct for ct, x in enumerate(tab.row(0)) if x.value not in ['', 1]] +
            range(self.label_row)
        )
        rem_cols = list(set(range(tab.ncols)) - ig_cols)
        ig_rows = set(
            [ct for ct, x in enumerate(tab.col(0)) if x.value not in ['', 1]] +
            range(self.header_rows)
        )
        rem_rows = list(set(range(tab.nrows)) - ig_rows)
        rem_cols.sort()
        rem_rows.sort()
        return rem_cols, rem_rows

    def absorb_data_columns(self, tab_name):
        """
        NB ignores headers and cols marked for hiding
        :param tab_name: string of the tab's name
        :return: each column of data in that tab
        """
        tab = self.book.sheet_by_name(tab_name)
        # return [self._one_data_column(tab, col_idx) for col_idx in range(tab.ncols)]
        ## tmp_cols = set(range(tab.ncols)) - self.ig_cols
        return [self._one_data_column(tab, col_idx) for col_idx in
                self.coro_idxs[tab_name][0]]

    def _one_data_column(self, tab, col_idx):
        """ignores headers and rows that are marked for hiding"""
        if self.use_pickle:
            return self.raw_data[tab][col_idx]
        else:
            # return tab.col(col_idx)[self.header_rows:]
            return [t for (c, t) in enumerate(tab.col(col_idx)) if c in
                    self.coro_idxs[tab.name][1]]

    # ============================
    # USEFUL FUNCTIONS
    # ============================
    def find_key(self, file_name):
        try:
            return [k for k in self.keys if k.name.startswith(
                os.path.splitext(file_name)[0])][0]
        except:
            return None

    def divert_on_pickle(self, res, key, failfn):
        """
        :param res: the instance attribute you want to set
        :param key: the s3 key / file
        :param failfn: fn to operate if no key
        :return: run of failfn
        """
        if self.use_pickle:
            try:
                setattr(self, res, pickle.loads(
                    self.find_key(key).get_contents_as_string())
                        )
            except:
                getattr(self, failfn)()
                self.use_pickle = False
        else:
            getattr(self, failfn)()

    # ================
    # HELPER FUNCTIONS
    # ================
    def _deco_p_test(func):
        """
        :return: tests if a pickle has been used; if so, returns error msg
        """
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            if self.use_pickle:
                print(self.pickle_e_msg.format(func.__name__))
            else:
                return func(self, *args, **kwargs)
        return wrapped

    @_deco_p_test
    def get_ctypes_by_ID(self, tab_name):
        """
        :param tab_name: The tab we're working with
        :return: For each column, every data-type showing up in the
        data section of that column
        """
        tab = self.book.sheet_by_name(tab_name)
        # return [set([cell.ctype for cell in col]) for col in cols]
        cols_data = [self._one_data_column(tab, col_idx) for col_idx in
                self.coro_idxs[tab_name][0]]
        return [set([cell.ctype for cell in col]) for col in cols_data]

    @_deco_p_test
    def get_cols(self, tab_name):
        """
        :param tab_name: The tab we're working with
        :return: column headers
        """
        # first headers have no prefix
        # second set iterate through prefixes A, B, C
        # truncating to length tab.ncols
        tab = self.book.sheet_by_name(tab_name)
        return (
            list(string.ascii_uppercase) + [
                string.ascii_uppercase[idx] + k for idx in range(
                        tab.ncols // len(string.ascii_uppercase))
                for k in list(string.ascii_uppercase)]
            )[:tab.ncols]

    # ================
    # SUPPORTING GET_CTYPES_BY_ID
    # ================
    @_deco_p_test
    def get_ctypes_by_name(self, tab_name):
        """
        :param tab_name: The tab we're working with
        :return: For each column, from data-types (in each col) to names
        """
        return [[self.type_codes[ele] for ele in col_set]
                for col_set in self.get_ctypes_by_ID(tab_name)]

    @_deco_p_test
    def get_ctype_bins(self, tab_name):
        """
        :param tab_name: The tab we're working with
        :return: For each column, give us 1/0s for presence/absence
        of each of proscribed types, eg each return is 010000
        """
        # combi_set = range(len(self.allowable_types))
        return [[(False, True).index(type_key in col_set) for type_key in
                 self.type_codes.keys()]
                for col_set in self.get_ctypes_by_ID(tab_name)]



"""
@_deco_p_test
def print_cytpes(self, tab_name):
    return zip(string.ascii_uppercase, self.get_ctypes_by_name(tab_name))

def absorb_data_rows(self, tab_name):
    NEEDS UPDATING FOR IGNORES
    ###
    ignores headers; convenience - not used
    :param tab_name: string of the tab's name
    ###
    tab = self.book.sheet_by_name(tab_name)
    # return [tab.row(row_idx) for row_idx in range(tab.nrows)][self.header_rows:]
    ## tmp_rows = set(range(tab.nrows)) - self.ig_rows
    return [tab.row(row_idx) for row_idx in self.rem_rows]
"""
