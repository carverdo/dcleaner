__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
import numpy as np
import string
import difflib

NO_BUCKETS = 12.0
STR_LEN_MAX = 400


class Digitize(object):
    """
    We have columns of unprocessed data (strings of lists in each column).
    Yuck; we need to process the data first.

    Next. Some rows are for training purposes and we use those to find
    the acceptable outer limits of data and to build bins.
    These bins are calculated by column (each a key) and set the
    limits for a digitisation process.

    Digitisation (a bit like histogramming) is an interim phase
    on the way to symbolisation. But symbolisation is just a way of
    getting the numerical base higher ie base 26 or 52 etc.
    to make comparisons easier (we do this later).
    """
    keys = ['acx', 'acy', 'theta', 'beta', 'gamma']
    ckeys = ['radius', 'angle']
    # number_to_letter function
    # outofsample data will end up in bucket zero and to the right of NO_BUCKETS;
    # eg with 3 buckets: 'a', 'bcd', 'e';
    symber = np.vectorize(lambda x: string.ascii_letters[x])

    def __init__(self, train_raw, ignores=0):
        """
        :param train_raw: string entries
        :param ignores: first N elements to ignore in each string_list
        :return: built-out training data set
        """
        self.train_data, self.bins = [], {}
        self.digiRows, self.symRows = [], []
        self.ignores = ignores
        self.build_from_train(train_raw)

    def build_from_train(self, train_raw):
        """
        Primary function, building bins and symbols around training data
        """
        for tr in train_raw:
            self.train_data.append(
                    self.process_data_row(tr)
            )
        self.build_bins()
        for row in self.train_data:
            self.build_syms(row)
            self.digiRows.append(self.digiRow)
            self.symRows.append(self.symRow)

    def build_test(self, test_raw):
        """
        :param test_raw: string(s) of test_data
        :return: test variants of digiRows and SymRows
        """
        test_digiRows, test_symRows = [], []
        for tr in test_raw:
            tmp = self.process_data_row(tr)
            self.build_syms(tmp)
            test_digiRows.append(self.digiRow)
            test_symRows.append(self.symRow)
        return test_digiRows, test_symRows

    def process_data_row(self, raw_row):
        """
        :param raw_data: strings from database to be turned into lists
        :return: list (one per row) of dictionaries (keys=column_headers)
        """
        r_tmp = {}
        for key in self.keys:
            one_row = self.clean_string(raw_row.__dict__[key])[self.ignores:]
            ## one_row = self.clean_string(raw_row[key])[self.ignores:]  ## xx
            if key == 'theta': one_row = map(self.oneighter, one_row)
            r_tmp[key] = one_row
        r_tmp['radius'] = self._add_rad(r_tmp['acx'], r_tmp['acy'])
        r_tmp['angle'] = self._add_tan(r_tmp['acx'], r_tmp['acy'])
        return r_tmp

    def build_bins(self):
        """For each key, generate bin limits based on block of training data"""
        for key in self.keys + self.ckeys:
            feat_col = [row[key] for row in self.train_data]
            self.bins[key] = np.arange(*self._bin_limits(feat_col))

    def build_syms(self, row):
        """Build symbol representation for each row and column of database"""
        self.digiRow, self.symRow = {}, {}
        for key in self.keys + self.ckeys:
            ar = row[key]
            bin_range = self.bins[key]
            self.gen_syms(key, ar, bin_range)

    def gen_syms(self, key, ar, bins):
        """Populate cell with key-driven digi,sym data"""
        self.digiRow[key] = np.digitize(ar, bins)
        self.symRow[key] = self.symber(self.digiRow[key])

    @staticmethod
    def clean_string(dirty_str):
        tmp = dirty_str[(dirty_str.index('[') + 1):dirty_str.index(']')].split(',')
        return np.array(map(float, tmp))

    @staticmethod
    def oneighter(deg):
        """we prefer degrees to be expressed in this way"""
        # oneighter = lambda self, x: x - 360 if x > 180 else x
        return deg - 360 if deg > 180 else deg

    @staticmethod
    def _add_rad(xs, ys):
        """Radius Calc"""
        return np.array(
                [np.round(np.sqrt(np.square(x) + np.square(y)), 2)
                 for x, y in zip(xs, ys)]
        )

    @staticmethod
    def _add_tan(xs, ys):
        """Angle Calc"""
        tmp = []
        for x, y in zip(xs, ys):
            if x == 0:
                if y == 0:
                    tmp.append(0.00)
                elif y > 0:
                    tmp.append(90.00)
                else:
                    tmp.append(-90.00)
            else:
                tmp.append(
                        np.round(np.arctan(y / x) * 180 / np.pi, 2)
                )
        return np.array(tmp)

    @staticmethod
    def _bin_limits(data):
        """Find maxmax and minmin of the training featureset"""
        bin_mn = min(min(ar) for ar in data)
        bin_mx = max(max(ar) for ar in data) + 0.01  # adjust for half-open
        bin_size = (bin_mx - bin_mn) / NO_BUCKETS
        return bin_mn, bin_mx, bin_size


class RunCompare(object):
    s = difflib.SequenceMatcher(None, autojunk=False)

    def __init__(self, exemplar, key, lenner=STR_LEN_MAX):
        """string b / sequence 2 is the important case; it stays still; 'a' varies."""
        self.s.set_seq2(self.recombine(exemplar[key][:lenner]))
        self.key = key
        self.lenner = lenner

    def run_comparison(self, choiceA):
        self.s.set_seq1(self.recombine(choiceA[self.key][:self.lenner]))
        return round(self.s.ratio(), 2)

    @staticmethod
    def recombine(x):
        return ''.join(map(str, x))


if __name__ == '__main__':
    import os

    os.chdir('..')
    os.chdir('..')
    fileObj = open('tests/raw.txt').readlines()
    fileObj = [ro.strip() for ro in fileObj]
    # fileObj has key, then 11 associated value entries
    # 6 of those 11 are training
    # we need to re-format to mimic raw_data
    train_data_rows = (0, 6)
    train_data = []
    for d in range(*train_data_rows):
        r = {}
        for idx in range(0, 60, 12):
            key = fileObj[idx]
            val_idx = idx + 1 + d
            val = fileObj[val_idx]
            r[key] = val
        train_data.append(r)
    dg = Digitize(train_data)

    aa = dg.digiRows
    # for obj in aa: print sum(obj['acx'])
    # see if matches excel
    # repeat with all keys
    bb = dg.symRows
    # for obj in bb: print obj['angle']
    # see if matches excel
    # repeat with all keys

    test_data_rows = (6, 11)
    test_data = []
    for d in range(*test_data_rows):
        r = {}
        for idx in range(0, 60, 12):
            key = fileObj[idx]
            val_idx = idx + 1 + d
            val = fileObj[val_idx]
            r[key] = val
        test_data.append(r)
    test_digiRows, test_symRows = dg.build_test(test_data)
    cc = test_digiRows
    for obj in cc: print sum(obj['angle'])
    # see if matches excel
    # repeat with all keys
    dd = test_symRows
    for obj in dd: print obj['acy']
    # see if matches excel
    # repeat with all keys
