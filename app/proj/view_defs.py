"""
CALCULATION SCRIPTS
Used for AJAX requests.
"""
__author__ = 'donal'
__project__ = 'dataHoover'

import string
from collections import Counter
from copy import deepcopy
import config_project
from . import fst


def build_label(idx_good_data):
    """
    :param idx_good_data: indexed list of data cells in column
    :return: string showing max, min and unique entries in the data
    """
    idx_good_data = [(pos, cell.value) for (pos, cell) in idx_good_data]
    idx_good_data.sort(key=lambda (pos, cell): cell)
    if idx_good_data:
        label_stats = {'min': idx_good_data[0], 'max': idx_good_data[-1]}
        # uniques / set / remove duplicate
        c_gdata = Counter(map(lambda (p, c): c, idx_good_data))
        unique_vals = filter(lambda k: c_gdata[k] == 1, c_gdata)
        label_stats['uniques'] = filter(lambda (p, c):
                                        c in unique_vals, idx_good_data)
    else:
        label_stats = {'min': 'na', 'max': 'na'}
    return label_stats


def build_outliers(idx_good_data, lenners=1):
    """
    :param idx_good_data: indexed list of data cells in column
    :param lenners: length of return
    :return: string showing max, min and unique entries in the data
    """
    idx_good_data.sort(key=lambda (pos, cell): cell.value)
    c_gdata = Counter(map(lambda (p, c): c.value, idx_good_data))
    unique_vals = filter(lambda k: c_gdata[k] == 1, c_gdata)
    unique_res = filter(lambda (p, c): c.value in unique_vals, idx_good_data)
    unique_res.sort()
    # we want to maintain order (otherwise would list(set()) )
    # max, min, uniques
    box = idx_good_data[:lenners]
    for obj in idx_good_data[-lenners:]:
        if obj not in box: box.append(obj)
    for obj in unique_res:
        if obj not in box: box.append(obj)
    return box


def _quick_label(tab_name, col_idx, label_stats=None):
    datapack = {'tab_name': tab_name, 'col_idx': col_idx, 'header': label_stats}
    label_base = '{t} {c} {rem}'.format(
            t=tab_name,
            c=string.ascii_uppercase[col_idx],
            rem='{r} | {ty} {v}'
    )
    return datapack, label_base


def _adjust_label(label_base, cell_data, header_rows, allowable_types):
    return label_base.format(
            r=cell_data[0] + 1 + header_rows,
            ty=allowable_types[cell_data[1].ctype],
            v=cell_data[1].value
    )


def get_nonfailed_cells_by_col(dh, tab, col_idx, row_labs):
    """
    :param dh: data-handled object
    :param tab: relevant tab
    :param col_idx: relevant column
    :param row_labs: the label filter
    :return: the nonfailed cells
    """
    col_data = list(enumerate(dh._one_data_column(tab, col_idx)))
    nonfailed_data = filter(lambda (idx, cell):
                            dh.type_codes[cell.ctype] not in row_labs, col_data)
    failed_data = list(set(col_data) - set(nonfailed_data))
    failed_data.sort()
    uniques = build_outliers(nonfailed_data)
    label_stats = build_label(nonfailed_data)
    return failed_data, uniques, label_stats


def ppack_em_up(tab_name, col_idx, tab_dict_col,
                idx_cells,
                header_rows, allowable_types):
    """
    :param tab_name: for labeling
    :param col_idx: for labeling
    :param tab_dict_col: dictionary of problem cells
    :param idx_cells: for iteration
    # :param label_stats: for headers / mouseovers
    :param header_rows: for labeling / filtering
    :param allowable_types: for labeling / filtering
    # :return: label plus form_dictionary which has been tailored (if possible)
    # to include a guess of the true value
    """
    tmp = []
    datapack, label_base = _quick_label(tab_name, col_idx)
    # build column of failed results -
    if tab_dict_col is not None:
        for cell_data in idx_cells:
            label = _adjust_label(label_base, cell_data,
                                  header_rows, allowable_types)
            for required in tab_dict_col:
                req_form = deepcopy(config_project.FORM_DICT_VARS[required])
                convert_instruction = 'to_{}'.format(required)
                if hasattr(fst, convert_instruction):
                    fst.run_parse(convert_instruction, cell_data[1].value)
                    req_form['value'] = fst.sec
                req_form['name'] += label.split(' | ')[0]
                tmp.append((label, req_form))
    datapack['ffails'] = tmp
    return datapack


def pack_em_up(tab_name, col_idx, tab_dict_col,
               idx_cells, label_stats,
               header_rows, allowable_types):
    """
    :param tab_name: for labeling
    :param col_idx: for labeling
    :param tab_dict_col: dictionary of problem cells
    :param idx_cells: for iteration
    :param label_stats: for headers / mouseovers
    :param header_rows: for labeling / filtering
    :param allowable_types: for labeling / filtering
    # :return: label plus form_dictionary which has been tailored (if possible)
    # to include a guess of the true value
    """
    tmp = []
    datapack, label_base = _quick_label(tab_name, col_idx, label_stats)
    # build column of outliers -
    for cell_data in idx_cells:
        label = _adjust_label(label_base, cell_data,
                              header_rows, allowable_types)
        for required in tab_dict_col:
            req_form = deepcopy(config_project.FORM_DICT_VARS[required])
            req_form['value'] = cell_data[1].value
            req_form['name'] += label.split(' | ')[0]
            tmp.append((label, req_form))
    datapack['outliers'] = tmp
    return datapack
