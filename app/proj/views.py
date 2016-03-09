__author__ = 'donal'
__project__ = 'dcleaner'
# todo Datahandler init is hardwired

import ast
from datetime import datetime
from flask import render_template, request, jsonify, json, flash
from flask.ext.login import current_user, login_required
from ..log_auth.views import login_confirmed
from config_project import VERSION, PROJECT_NAME
from . import proj, DataHandler
# helper functions -
from view_defs import get_nonfailed_cells_by_col, ppack_em_up, pack_em_up
from app.updown.views import user_driven_connect
from app.proj.data_handler2 import DataHandler2
from app.templates.flash_msg import *

# ========================
# FUNCTIONS
# ========================
def name_stamp(filename):
    return '{}_{}_{}_{}_{}.txt'.format(
            filename, current_user.firstname, PROJECT_NAME, VERSION,
            datetime.now().strftime('%Y%m%d_%H%M%S'))


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
@proj.route('/prim_view')
@login_confirmed
def prim_view():
    sh = user_driven_connect()
    dh = DataHandler2(sh.keys, header_rows=2, label_row=1)
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
                           data_dict=dh.html_pack
                           )


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
    data_dict = json.loads(request.get_data())
    # test emptiness of first value
    if bool(data_dict.values()[0]):
        sh = user_driven_connect()
        dh = DataHandler2(sh.keys, header_rows=2, label_row=1)
        # dh = DataHandler(header_rows=2)  # 'app/static/data/{}.xls'.format(EXCEL_SOURCE),
        dh.package_for_html()
        # datapacks = []
        nonfail_packs, ffail_packs = [], []
        for tab_name, tab_dict in data_dict.items():
            # read new worksheet
            # tab = dh.book.sheet_by_name(tab_name)
            tmp_refs = {}
            # build register
            for row_lab, cols in filter(lambda (k, v):
                                        not k.isdigit(), tab_dict.items()):
                for col_idx in cols:
                    tmp_refs.setdefault(col_idx, []).append(row_lab)
            # build our nonfail_ and fail_packs
            for col_idx, row_labs in tmp_refs.iteritems():
                fail_pack, nonfail_pack, label_stats = \
                    get_nonfailed_cells_by_col(dh, tab_name, col_idx, row_labs)
                nonfail_packs.append(pack_em_up(
                    tab_name, col_idx, tab_dict.get(str(col_idx), None),
                    nonfail_pack, label_stats,
                    dh.header_rows, dh.allowable_types
                ))
                ffail_packs.append(ppack_em_up(
                    tab_name, col_idx, tab_dict.get(str(col_idx), None),
                    fail_pack,
                    dh.header_rows, dh.allowable_types
                ))
    else:
        nonfail_packs = None
        ffail_packs = [{'tab_name': 'na',
                        'col_idx': 'na',
                        'header': {'empty': 'na'},
                        'ffails': []
                        }]
    return jsonify(ffail_pack=ffail_packs,
                   nonfail_pack=nonfail_packs)


@proj.route('/_stamp', methods=["GET", "POST"])
@login_required
def _stamp():
    data = json.loads(request.get_data())
    sh = user_driven_connect()
    if sh:
        msg = sh.s3_upload(name_stamp('Stamp_Vers'),
                           upload_fn='string', str_data=str(data))
        flash(msg)
    return jsonify(result=data)


@proj.route('/_load_stamp_list', methods=["GET", "POST"])
@login_required
def _load_stamp_list():
    # data = request.get_data()
    sh = user_driven_connect()
    if sh:
        res = [k.name for k in sh.keys if k.name.startswith('Stamp_Vers')]
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
    data = json.loads(request.get_data())
    sh = user_driven_connect()
    if sh:
        msg = sh.s3_upload(name_stamp('Logged_Data'),
                           upload_fn='string', str_data=str(data))
        flash(msg)
    return jsonify(result=data)


"""
@proj.route('/home3')
@login_confirmed
def bosh():
    dh = DataHandler('app/static/data/{}.xls'.format(EXCEL_SOURCE),
                     header_rows=2, label_row=1)
    dh.package_for_html()
    return render_template('./proj/prim_view.html',
                           summary=dh.summary,
                           data_dict=dh.html_pack
                           )
"""
"""
@proj.route('/_load_stamp', methods=["GET", "POST"])
def _load_stamp():
    data = request.get_data()
    sh = user_driven_connect()
    if sh:
        print sh.keys
    return jsonify(result=TypeStamper().load_choices(data.split("\\")[-1]))
"""

"""
@proj.route('/prim_view')
@login_confirmed
def prim_view():
    dh = DataHandler(header_rows=2, label_row=1)
    if dh.file_name: dh.package_for_html()
    return render_template('./proj/prim_view.html',
                           usr_data='{} | {}_v{}'.format(
                                   current_user.firstname,
                                   PROJECT_NAME, VERSION),
                           summary=dh.summary,
                           data_dict=dh.html_pack
                           )
"""