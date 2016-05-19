"""

"""
__author__ = 'donal'
__project__ = 'dcleaner'
# todo Datahandler init is hardwired
# todo rows and columns hardwired
# todo find_last_log doesn't know that there are multi projects

import ast
from flask import render_template, request, jsonify, json, flash, redirect, \
    url_for, current_app
from flask.ext.login import current_user, login_required
from ..log_auth.views import login_confirmed
from config_project import VERSION, PROJECT_NAME
from . import proj, DataHandler2
# helper functions -
from view_defs import parse_cells, ppack_em_up, pack_em_up, \
    name_stamp, curr_logins, find_last_log, log_reduce
from app.updown.views import user_driven_connect
from app.templates.flash_msg import *
from app.log_auth.views import set_template


# ========================
# SIMPLE STUFF
# ========================
@proj.route('/')
@proj.route('/home2')
@login_confirmed
def home2():
    return render_template('./proj/dummy.html')


@proj.route('/getting_started')
@login_confirmed
def getting_started():
    return render_template('./proj/gettingStarted.html')


@proj.route('/picture')
@login_confirmed
def picture():
    return render_template('./proj/picture.html')


# =================================================
# TRICKIER / MAIN PAGE
# =================================================
@proj.route('/data_sets', methods=['GET', 'POST'])
@login_confirmed
def data_sets():
    if request.method == 'POST':
        return redirect(url_for('.prim_view', fname=request.form['fname']))
    return set_template('panelbuilder.html', None, '',
                        panel_args=dict(
                            patex=current_app.config['PAHDS']['projset'],
                            tadata=current_app.config['TADATA']['projset']
                        ))


@proj.route('/prim_view/<fname>', methods=['GET', 'POST'])
@login_confirmed
def prim_view(fname):
    current_user.ping(increment=False)
    sh = user_driven_connect()
    dh = DataHandler2(sh.keys, file_name=fname)  # , header_rows=2, label_row=1)
    if dh.key:
        if not dh.find_key(dh.p_summ):
            sh.s3_upload(dh.p_summ, upload_fn='string', str_data=dh.tmp_s)
            flash(f72.format(dh.p_summ))
        if not dh.find_key(dh.p_data):
            dh.package_for_html()
            sh.s3_upload(dh.p_data, upload_fn='string', str_data=dh.tmp_d)
            flash(f72.format(dh.p_data))
            sh.s3_upload(dh.p_html, upload_fn='string', str_data=dh.tmp_h)
            flash(f72.format(dh.p_html))
        else:
            dh.package_for_html()
    return render_template('./proj/prim_view.html',
                           usr_data='{} | {}_v{}'.format(
                                   current_user.firstname,
                                   PROJECT_NAME, VERSION),
                           summary=dh.summary,
                           data_dict=dh.html_pack,
                           curr_logins=curr_logins()
                           )


@proj.route('/logs_view')
@login_confirmed
def logs_view():
    current_user.ping(increment=False)
    sh = user_driven_connect()
    if sh:
        priors = find_last_log(sh).split('||')[1:]
    else: priors = 'none available'
    return render_template('./proj/datalogs.html', data=priors)


# =================================================
# AJAX REQUESTS
# =================================================
@proj.route('/_bosh', methods=["GET", "POST"])
@login_required
def _bosh():
    """
    This function is called by genUnfitData.
    That data is processed here, and, if desired, sent back.
    """
    # data_dict has only one key (the clicked Tab)
    dset, data_dict, threshes = json.loads(request.get_data())
    # test emptiness of first value
    if bool(data_dict.values()[0]):
        sh = user_driven_connect()
        dh = DataHandler2(sh.keys, file_name=dset)  # , header_rows=2, label_row=1)
        dh.package_for_html()
        prior_logs = log_reduce(sh, dset)
        ffail_packs, nonfail_packs, gapper = [], [], []
        for tab_name, tab_dict in data_dict.items():
            # read new worksheet
            # tab = dh.book.sheet_by_name(tab_name)
            tmp_refs = {}
            rem_cols, rem_rows = dh.html_pack[tab_name]['coro_idxs']
            # build register
            for row_lab, cols in filter(lambda (k, v):
                                        not k.isdigit(), tab_dict.items()):
                for col_idx in cols:
                    tmp_refs.setdefault(col_idx, []).append(row_lab)
            # build our nonfail_ and fail_packs
            for col_idx, row_labs in tmp_refs.iteritems():
                col_mapped = rem_cols[col_idx]
                fail_pack, nonfailer, label_stats = parse_cells(
                    dh, tab_name, col_idx, rem_rows, row_labs, threshes)

                tab_dict_col = tab_dict.get(str(col_idx), None)
                if tab_dict_col:
                    nonfail_pack, gaps = nonfailer
                    ffail_packs.append(ppack_em_up(
                        tab_name, col_idx, col_mapped,
                        tab_dict_col,
                        fail_pack, prior_logs,
                        dh.header_rows, dh.allowable_types
                    ))
                    nonfail_packs.append(pack_em_up(
                        tab_name, col_idx, col_mapped,
                        tab_dict_col,
                        nonfail_pack, prior_logs,
                        label_stats,  # not in previous def
                        dh.header_rows, dh.allowable_types
                    ))
                    gapper.append(gaps)
    else:
        ffail_packs = [{'tab_name': 'na',
                        'col_idx': 'na',
                        'header': {'empty': 'na'},
                        'ffails': []
                        }]
        nonfail_packs = [{'outliers': []}]
        gapper = []
    return jsonify(ffail_pack=ffail_packs,
                   nonfail_pack=nonfail_packs,
                   gapper=gapper)


@proj.route('/_stamp', methods=["GET", "POST"])
@login_required
def _stamp():
    dset, data = json.loads(request.get_data())
    sh = user_driven_connect()
    if sh:
        msg = sh.s3_upload(name_stamp('Stamp_Vers_{}'.format(dset.upper())
                                      ),
                           upload_fn='string', str_data=str(data))
        flash(msg)
    return jsonify(result=data)


@proj.route('/_load_stamp_list', methods=["GET", "POST"])
@login_required
def _load_stamp_list():
    dset = request.get_data()
    sh = user_driven_connect()
    if sh:
        res = [k.name for k in sh.keys if k.name.startswith(
                'Stamp_Vers_{}'.format(dset.upper())
        )]
        return jsonify(result=res)
    else: return jsonify(result=None)


@proj.route('/_load_stampB', methods=["GET", "POST"])
@login_required
def _load_stampB():
    data = request.get_data()
    sh = user_driven_connect()
    key = sh.bucketconn.get_key(data)
    res = map(float, ast.literal_eval(key.read()))
    return jsonify(result=res)


@proj.route('/_logcache', methods=["GET", "POST"])
@login_required
def _logcache():
    dset, data = json.loads(request.get_data())
    sh = user_driven_connect()
    if sh:
        tmp = find_last_log(sh, dset)
        if tmp: data = tmp + '\n\n' + data
        msg = sh.s3_upload(name_stamp('Logged_Data_{}'.format(dset.upper())
                                      ),
                           upload_fn='string', str_data=str(data))
        flash(msg)
    return jsonify(result=data)
