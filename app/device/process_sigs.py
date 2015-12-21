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

    def __init__(self, raw_data, ignores=0):
        self.all_raw = []
        self.bins = {}
        self.digiRows, self.symRows = [], []
        self.proc_data(raw_data, ignores)
        self.build_bins()
        self.runner()

    def proc_data(self, raw_data, ignores):
        """
        :param raw_data: strings from database to be turned into lists
        :param ignores: first N elements to ignore in each string_list
        :return: list (one per row) of dictionaries (keys=column_headers)
        """
        def clean_string(dirty_str):
            return dirty_str[(dirty_str.index('[')+1):dirty_str.index(']')].split(',')

        for r in raw_data:
            r_tmp = {}
            for key in self.keys:
                one_row = clean_string(r.__dict__[key])[ignores:]
                one_row = np.array(map(float, one_row))
                if key == 'theta': one_row = map(self.oneighter, one_row)
                r_tmp[key] = one_row
            r_tmp['radius'] = self._add_rad(r_tmp['acx'], r_tmp['acy'])
            r_tmp['angle'] = self._add_tan(r_tmp['acx'], r_tmp['acy'])
            self.all_raw.append(r_tmp)

    def build_bins(self):
        """For each key, generate bin limits based on block of training data"""
        for key in self.keys + self.ckeys:
            feat_col = [row[key] for row in self.all_raw]
            self.bins[key] = np.arange(*self._bin_limits(feat_col))

    def runner(self):
        """Build symbol representation for each row and column of database"""
        for row in self.all_raw:
            self.digiRow, self.symRow = {}, {}
            for key in self.keys + self.ckeys:
                ar = row[key]
                bin_range = self.bins[key]
                self.gen_syms(key, ar, bin_range)
            self.digiRows.append(self.digiRow)
            self.symRows.append(self.symRow)

    def gen_syms(self, key, ar, bins):
        """Populate cell with key-driven digi,sym data"""
        self.digiRow[key] = np.digitize(ar, bins)
        self.symRow[key] = self.symber(self.digiRow[key])

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
                if y == 0: tmp.append(0.00)
                elif y > 0: tmp.append(90.00)
                else: tmp.append(-90.00)
            else:
                tmp.append(
                        np.round(np.arctan(y / x) * 180 / np.pi, 2)
                )
        return np.array(tmp)

    @staticmethod
    def _bin_limits(data):
        """Find maxmax and minmin of the featureset"""
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
