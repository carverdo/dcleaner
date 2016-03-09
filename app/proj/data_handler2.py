import pickle
import string
from functools import wraps
import os
import xlrd
from config_project import EXCEL_ALLOWABLE_TYPES, EXCEL_SOURCE

# todo xlrd only looks to xls files; need to investigate other readers.
# todo namedTuples simplified things in tiab_processing/parse_exTab

__author__ = 'donal'
__project__ = 'dcleaner'


class DataHandler2(object):
    allowable_types = EXCEL_ALLOWABLE_TYPES
    type_codes = dict(enumerate(allowable_types))
    pickle_e_msg = 'WARNING: method <{}> not run. ' \
                   'You need to reload class with use_pickle=False'

    def __init__(self, keys, file_name=EXCEL_SOURCE,
                 header_rows=1, label_row=0,
                 use_pickle=True):
        # classic inits
        self.keys = keys
        self.header_rows,  self.label_row = header_rows, label_row
        self.use_pickle = use_pickle
        # s3 stores of keys and their data
        self.p_summ, self.p_data, self.p_html = None, None, None
        self.tmp_s, self.tmp_d, self.tmp_h = None, None, None
        # local vars
        self.book, self.summary = None, {}
        self.raw_data, self.html_pack = {}, {}
        # snapshot of basic data (only snapshot for now; speed)
        self.key = self.find_key(file_name)
        if self.key:
            self.build_subkeys()
            self.build_summary()

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
        """
        self.divert_on_pickle('summary', self.p_summ, '_build_summary')

    def _build_summary(self):
        """
        :return: summary of the worksheets; intake of summary data;
        pickles the object afterwards.
        """
        # first, grab file metadata; then inspect
        self.summary['meta'] = self.key.etag[1:-1], self.key.last_modified
        print '.'
        self.book = xlrd.open_workbook(file_contents=
                                       self.key.get_contents_as_string())
        self.summary['WorkBook'] = {
            'COLUMNS assumed/HEADER DEPTH': 'x{} ROW'.format(self.header_rows),
            '# tabs': self.book.nsheets,
            'tab names': self.book.sheet_names(),
        }
        active_tabs = []
        for tab in self.book.sheets():
            if tab.nrows >= self.header_rows:
                self.summary[tab.name] = {
                    'cols by rows': '{} by {}'.format(tab.ncols, tab.nrows),
                    'column_headers': tab.row(self.label_row)
                }
                active_tabs.append(tab.name)
            else:
                self.summary[tab.name] = {'cols by rows': 'EMPTY'}
        self.summary['active_tabs'] = active_tabs
        print '_b_summ'
        self.tmp_s = pickle.dumps(self.summary, -1)

    # ============================
    # B. HTML OUTPUT
    # part 1 for pickle; part 2 if doing for first time
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
            tab = self.book.sheet_by_name(tab_name)
            self.html_pack[tab_name] = {
                'tab': tab_name,
                'headers': zip(
                        self.get_cols(tab_name),
                        [tab.cell(self.label_row, col_idx) for col_idx
                         in range(tab.ncols)]
                ),
                'data': data
            }
        print '_b_pfhtml'
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
                self.raw_data[tab.name] = self.absorb_data_columns(tab.name)
            else: pass
        print '_b_raw'
        self.tmp_d = pickle.dumps(self.raw_data, -1)

    # ============================
    # USEFUL FUNCTIONS
    # ============================
    def find_key(self, file_name):
        try:
            return [k for k in self.keys if k.name.startswith(
                    os.path.splitext(file_name)[0])][0]
        except: return None

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
                print 'laded', key
            except:
                print 'ee'
                getattr(self, failfn)()
                self.use_pickle = False
                print 'exc didnt load'
        else:
            print 'else pickleoff'
            getattr(self, failfn)()

    def absorb_data_columns(self, tab_name):
        """
        NB ignores headers.
        :param tab_name: string of the tab's name
        :return: each column of data in that tab
        """
        tab = self.book.sheet_by_name(tab_name)
        return [self._one_data_column(tab, col_idx)
                for col_idx in range(tab.ncols)]

    def absorb_data_rows(self, tab_name):
        """
        ignores headers; convenience - not used
        :param tab_name: string of the tab's name
        """
        tab = self.book.sheet_by_name(tab_name)
        return [tab.row(row_idx)
                for row_idx in range(tab.nrows)][self.header_rows:]

    # ================
    # HELPER FUNCTIONS
    # ================
    def _one_data_column(self, tab, col_idx):
        """ignores headers"""
        if self.use_pickle:
            return self.raw_data[tab][col_idx]
        else:
            return tab.col(col_idx)[self.header_rows:]

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
        return [set(tab.col_types(col)[self.header_rows:])
                for col in range(tab.ncols)]

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

    @_deco_p_test
    def get_cols(self, tab_name):
        """
        :param tab_name: The tab we're working with
        :return: column headers
        """
        tab = self.book.sheet_by_name(tab_name)
        return list(string.ascii_uppercase[:tab.ncols])

    @_deco_p_test
    def print_cytpes(self, tab_name):
        return zip(string.ascii_uppercase, self.get_ctypes_by_name(tab_name))
