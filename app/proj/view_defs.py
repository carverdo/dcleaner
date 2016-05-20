"""
CALCULATION SCRIPTS
"""
__author__ = 'donal'
__project__ = 'dataHoover'

from datetime import datetime, timedelta
from operator import itemgetter
from flask.ext.login import current_user
from app.db_models import Member
from config_project import PROJECT_NAME, VERSION
from collections import Counter
from copy import deepcopy
import config_project
from . import fst
from app import lg
from data_handler2 import build_excel_col_headers


# =====================
# FILTERING COLUMN DATA
# =====================
def parse_cells(dh, tab_name, col_idx,
                rem_rows, row_labs, threshes, prior_snips, label_base2):
    """
    :param dh: data-handled object
    :param tab_name: relevant tab
    :param col_idx: relevant column
    :param rem_rows: [xxx]
    :param row_labs: the label filter
    :param threshes: lower, then upper value
    :param prior_snips: previously logged addresses
    :param label_base2: template string to be formatted
    :return: the typeFails, outliers, label headers
    """
    idx_cells = zip(rem_rows, dh._one_data_column(tab_name, col_idx))
    idx_cells = [cell_data for cell_data in idx_cells if
                 _adjust_label2(label_base2, cell_data) not in prior_snips]
    # parse by type
    nonfails = filter(lambda (idx, cell):
                      dh.type_codes[cell.ctype] not in row_labs, idx_cells)
    typeFails = list(set(idx_cells) - set(nonfails))
    typeFails.sort()
    # now look to values
    thresh_uniques = _build_outliers(nonfails, *threshes)
    label_stats = _build_label(nonfails)
    return typeFails, thresh_uniques, label_stats


# =====================
# PARSE CELL HELPERS
# =====================
def _adjust_label2(label_base, cell_data):
    return label_base.format(
            r=cell_data[0] + 1,  # EXCEL STARTS AT 1
    ).strip()


def _build_label(idx_good_data):
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


def _build_outliers(idx_good_data, lower, upper, badval, lenners=1):
    """
    :param idx_good_data: indexed list of data cells in column
    :param lower: user entered lower thresh
    :param upper: user entered upper thresh
    :param badval: user entered bad values
    :param lenners: length of return
    :return: string showing max, min and unique entries in the data
    """
    idx_good_data.sort(key=lambda (pos, cell): cell.value)
    # we want to maintain order (otherwise would list(set()) )
    # cutouts, max, min, uniques
    box = _build_threshers(idx_good_data, lower, upper, badval)
    gaps = [len(box)]
    for obj in idx_good_data[:lenners] + idx_good_data[-lenners:]:
        if obj not in box: box.append(obj)
    gaps.append(len(box))
    for obj in _build_uniques(idx_good_data):
        if obj not in box: box.append(obj)
    gaps.append(len(box))
    return box, gaps


def _build_threshers(idx_good_data, lower, upper, badval):
    lower, upper, badval = _numfix(lower), _numfix(upper), _numfix(badval)
    los, ups, bvals = [], [], []
    if lower or lower==0: los = filter(lambda (p, c): c.value < lower,
                                       idx_good_data)
    if upper or upper==0: ups = filter(lambda (p, c): c.value > upper,
                                       idx_good_data)
    if badval or badval==0: bvals = filter(lambda (p, c): c.value == badval,
                                           idx_good_data)
    cutout_res = list(set(los + ups + bvals))
    cutout_res.sort()
    return cutout_res


def _numfix(x):
    try: return float(x)
    except: return x


def _build_uniques(idx_good_data):
    c_gdata = Counter(map(lambda (p, c): c.value, idx_good_data))
    unique_vals = filter(lambda k: c_gdata[k] == 1, c_gdata)
    unique_res = filter(lambda (p, c): c.value in unique_vals, idx_good_data)
    unique_res.sort()
    return unique_res


# =====================
# PACKAGING COLUMN DATA
# =====================
def _adjust_label(label_base, cell_data, allowable_types):
    if isinstance(cell_data[1].value, basestring):
        cdv = cell_data[1].value.encode('ascii', 'replace')
    else: cdv = cell_data[1].value
    return label_base.format(
            r=cell_data[0] + 1,  # EXCEL STARTS AT 1
            ty=allowable_types[cell_data[1].ctype],
            v=cdv
    ).strip()


def ppack_em_up(tab_dict_col, idx_cells,
                label_base, allowable_types, datapack):
    """
    :param tab_dict_col: dictionary of problem cells
    :param idx_cells: for iteration
    :param label_base: to be adjusted per cell
    :param allowable_types: for labeling / filtering
    :param datapack: container
    :return: # column of failed results
    """
    tmp = []
    for cell_data in idx_cells:
        label = _adjust_label(label_base, cell_data, allowable_types)
        for required in tab_dict_col:
            req_form = deepcopy(config_project.FORM_DICT_VARS[required])
            convert_instruction = 'to_{}'.format(required)
            if hasattr(fst, convert_instruction):
                # todo prints False; problem?
                _ = fst.run_parse(convert_instruction, cell_data[1].value)
                req_form['value'] = fst.sec
            req_form['name'] += label.split(' | ')[0]
            tmp.append((label, req_form))
    datapack['ffails'] = tmp
    return datapack


def pack_em_up(tab_dict_col,idx_cells, label_stats,
               label_base, allowable_types, datapack):
    """
    :param tab_dict_col: dictionary of problem cells
    :param idx_cells: for iteration
    :param label_stats: for headers / mouseovers
    :param label_base: to be adjusted per cell
    :param allowable_types: for labeling / filtering
    :param datapack: container
    :return: column of outliers
    """
    tmp = []
    for cell_data in idx_cells:
        label = _adjust_label(label_base, cell_data, allowable_types)
        for required in tab_dict_col:
            req_form = deepcopy(config_project.FORM_DICT_VARS[required])
            req_form['value'] = cell_data[1].value
            req_form['name'] += label.split(' | ')[0]
            tmp.append((label, req_form))
    datapack['outliers'] = tmp
    datapack['headers'] = label_stats
    return datapack


# =====================
# PREVIOUSLY LOGGED ENTRIES
# =====================
def find_last_log(sh, dset=None, variant_1='%Y-%m-%dT%H:%M:%S.000Z'):
    # variant_2 = '%a, %d %b %Y %H:%M:%S GMT'
    if dset != None: nam = 'Logged_Data_{}'.format(dset.upper())
    else: nam = 'Logged_Data'
    logs = filter(lambda k: k.name.startswith(nam), sh.keys)
    if not logs: return None
    last_logs = [k.last_modified for k in logs]
    try:
        last_logs = [datetime.strptime(lalo, variant_1) for lalo in last_logs]
        return max(zip(last_logs, logs), key=itemgetter(0)
                   )[1].get_contents_as_string()
    except:
        return None


def log_reduce(sh, dset=None, fragOnly=True):
    priors, tmp = [], find_last_log(sh, dset)
    prior_snips = []
    if tmp:
        all_logs = tmp.split('|||')[1:]
        for log in all_logs:
            # cell data only
            each_sub = log.split('||')[1]
            # address fragments
            for frag in each_sub.split('\n')[:-1]:
                if fragOnly:
                    frag = frag.split(' | LOGGED |')[0].strip()
                    priors.append(frag)
                    """
                    t_key, c_key, value = frag.split(' | ')[0].split(' ')
                    prior_snips.setdefault(t_key, []).append(
                        ''.join((c_key, value))
                    )
                    """
                    prior_snips.append(frag.split(' | ')[0])
                else:
                    priors.append(frag.strip())
    return priors, prior_snips


# =====================
# HELPERS
# =====================
def name_stamp(filename):
    return '{}_{}_{}_{}_{}.txt'.format(
            filename, current_user.firstname, PROJECT_NAME, VERSION,
            datetime.now().strftime('%Y%m%d_%H%M%S'))


def curr_logins():
    an_hour_ago = datetime.utcnow() - timedelta(seconds=3600)
    most_recents = [m.email for m in Member.query.filter(
            Member.last_log>an_hour_ago).all()]
    return ' | '.join(most_recents)


def quick_label(tab_name, col_idx, col_mapped, label_stats=None):
    datapack = {'tab_name': tab_name, 'col_idx': col_idx, 'header': label_stats}
    label_base = '{t} {c} {rem}'.format(
            t=tab_name,
            #todo MODULAR MATH FIX BELOW FOR WIDE DATA
            c=build_excel_col_headers(col_mapped + 1)[-1], ## string.ascii_uppercase[col_idx],
            rem='{r} | {ty} {v}'
    )
    label_base2 = '{t} {c} {rem}'.format(
        t=tab_name,
        c=build_excel_col_headers(col_mapped + 1)[-1],
        rem='{r}'
    )
    return datapack, label_base, label_base2