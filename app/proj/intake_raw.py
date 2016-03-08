"""
Imports raw excel data from a given source.

The handler automatically pickles the result into two similarly named
pickle files (one for summary; one for raw_data).

The original data file is no longer used UNLESS explicitly instructed.
In other words, as long as those pickles are present, the xls is no longer
needed.
"""
__author__ = 'donal'
__project__ = 'dataHoover'
# todo xlrd only looks to xls files; need to investigate other readers.
# todo namedTuples simplified things in tiab_processing/parse_exTab
import pickle
import string
import xlrd
from config_project import *
from functools import wraps


class DataHandler2(object):
    allowable_types = EXCEL_ALLOWABLE_TYPES
    type_codes = dict(enumerate(allowable_types))
    pickle_e_msg = 'WARNING: method <{}> not run. ' \
                   'You need to reload class with use_pickle=False'

    def __init__(self, file_name=EXCEL_SOURCE,
                 header_rows=1, label_row=0,
                 use_pickle=True):
        # just make sure that there is a download directory in place
        # move to it, find our file
        if not os.path.exists(DL_DIR): os.makedirs(DL_DIR)
        self.dl_dir = DL_DIR

class DataHandler(object):
    """
    *** NOTE: the ASSUMPTION that IDs map to allowable_types ***

    header_rows is like length, ie the number of rows that are headers;
    label_row is a counter, starting at zero.
    """
    allowable_types = EXCEL_ALLOWABLE_TYPES
    type_codes = dict(enumerate(allowable_types))
    pickle_e_msg = 'WARNING: method <{}> not run. ' \
                   'You need to reload class with use_pickle=False'

    def __init__(self, file_name=EXCEL_SOURCE,
                 header_rows=1, label_row=0,
                 use_pickle=True):
        # just make sure that there is a download directory in place
        # move to it, find our file
        if not os.path.exists(DL_DIR): os.makedirs(DL_DIR)
        os.chdir(DL_DIR)
        self.file_name = os.path.join(
                DL_DIR,
                filter(lambda f: f.startswith(file_name) and
                       os.path.splitext(f)[1] == EXCEL_SUFFIX,
                       os.listdir(DL_DIR)
                       )[0]
        )
        # stores of data
        self.p_summ = os.path.splitext(file_name)[0] + '_summ.p'
        self.p_data = os.path.splitext(file_name)[0] + '_data.p'
        self.p_html = os.path.splitext(file_name)[0] + '_html.p'
        # classic inits
        self.header_rows = header_rows
        self.label_row = label_row
        self.use_pickle = use_pickle
        # snapshot of basic data (only snapshot for now; speed)
        self.book, self.summary = None, {}
        self.build_summary()
        # for later, raw_data generation
        self.raw_data, self.html_pack = {}, {}

    # ============================
    # A. GENERATING SUMMARY DATA
    # part 1 for pickle; part 2 if doing for first time
    # ============================
    def build_summary(self):
        """
        optionally chooses from the pickle of the same name;
        """
        if self.use_pickle:
            try:
                self.summary = pickle.load(open(self.p_summ, 'rb'))
            except:
                self._build_summary()
                self.use_pickle = False
        else:
            self._build_summary()

    def _build_summary(self):
        """
        :return: summary of the worksheets; intake of summary data;
        pickles the object afterwards.
        """
        # first, grab file metadata; then inspect
        self.summary['meta'] = os.stat(self.file_name)
        self.book = xlrd.open_workbook(self.file_name)
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
        pickle.dump(self.summary, open(self.p_summ, 'wb'), -1)

    # ============================
    # B. HTML OUTPUT
    # part 1 for pickle; part 2 if doing for first time
    # ============================
    def package_for_html(self):
        """
        optionally chooses from the pickle of the same name;
        """
        if self.use_pickle:
            try:
                self.raw_data = pickle.load(open(self.p_data, 'rb'))
                self.html_pack = pickle.load(open(self.p_html, 'rb'))
            except:
                self._package_for_html()
                self.use_pickle = False
        else:
            self._package_for_html()

    def _package_for_html(self):
        if not self.raw_data:
            self.build_raw_data()
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
        pickle.dump(self.html_pack, open(self.p_html, 'wb'), -1)

    # ============================
    # C. GENERATING RAW DATA
    # part 1 for pickle; part 2 if doing for first time
    # ============================
    def build_raw_data(self):
        """
        optionally chooses from the pickle of the same name;
        """
        if self.use_pickle:
            try:
                self.raw_data = pickle.load(open(self.p_data, 'rb'))
            except:
                self._build_raw()
                self.use_pickle = False
        else:
            self._build_raw()

    def _build_raw(self):
        """
        only builds from sheets where data present.
        pickles the object afterwards.
        """
        for tab in self.book.sheets():
            if tab.nrows >= self.header_rows:
                self.raw_data[tab.name] = self.absorb_data_columns(tab.name)
            else:
                pass
        pickle.dump(self.raw_data, open(self.p_data, 'wb'), -1)

    # ============================
    # USEFUL FUNCTIONS
    # ============================
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


if __name__ == '__main__':
    from pprint import pprint
    dh = DataHandler('../static/data/RawData.xls', header_rows=2,
                     use_pickle=False)
    dh.package_for_html()
    print """
    We have: dh.raw_data for the data section of every tab;
    We can address any cell;
    We can summarise data-types per column.
    """
    # make sure to pick a real tab!
    tab_name = 'CM'
    # because we load without pickle...
    # ie certain functions (decorated) only to be run in live case
    # where we have a true xlrd object in memory
    tmp_ok = dh.get_ctypes_by_ID(tab_name)
    tmp_ok2 = dh.get_ctypes_by_name(tab_name)
    print tmp_ok
    print tmp_ok2
    tab = dh.book.sheet_by_name(tab_name)
    pprint(dh.print_cytpes(tab_name))
    tmp = dh.absorb_data_columns(tab_name)
    print tmp[2]
    tamp = dh.absorb_data_rows(tab_name)
    print tamp[0]
    print '===='
    # instead, load without pickle...
    dh2 = DataHandler('../static/data/RawData.xls', header_rows=2)
    dh2.package_for_html()
    # because we used the pickle...
    tmp_fail = dh2.get_ctypes_by_ID(tab_name)
