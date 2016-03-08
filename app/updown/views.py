"""
Manage s3 uploads and downloads.
Not quite finished: tidy up the s3 defs and put into class.
"""
__author__ = 'donal'
__project__ = 'dcleaner'
from StringIO import StringIO
from collections import Counter
from flask.ext.login import current_user, login_required
from flask import render_template, request, flash, redirect, url_for, \
    current_app, send_file
from sqlalchemy import desc
from . import updo
from ..log_auth.views import admin_required
from app.templates.flash_msg import *
from config_vars import AWS_KEYS
from forms import DataUploadForm, BucketMap
from app.db_models import MemberBucketStore, Member
from config_project import EXCEL_BASE_DIR
from key_rotate import KeyRotation
from s3_handler import s3Handler


# ==================================================
# FUNCTIONS
# ==================================================
def user_driven_connect():
    """
    Adapt your connection based upon user;
    """
    try:
        if not current_user.adminr:
            row = MemberBucketStore.query.filter_by(member_id=current_user.id).\
                order_by(desc(MemberBucketStore.id)).first()
            return s3Handler(row.access_key_id, row.secret_access_key,
                             row.bucket)
        else: return s3Handler(AWS_KEYS['S3_KEY'], AWS_KEYS['S3_SECRET'],
                         EXCEL_BASE_DIR)
    except:  # if it has not been bucket-mapped, row returns empty
        flash(f170.format('access S3'))
        return None


# Gets addressing because it uses the browser for downloading
@updo.route('/s3_downloader/<path:s_name>')
@login_required
def s3_downloader(s_name):
    try:
        sh = user_driven_connect()
        key = sh.bucketconn.get_key(s_name)
        # In-memory file save
        buffer = StringIO()
        key.get_contents_to_file(buffer)
        buffer.seek(0)
        flash(f72.format(s_name))
        return send_file(buffer, as_attachment=True, attachment_filename=s_name)
    except:
        flash(f170.format('download data'))


# ==================================================
# VIEWS
# ==================================================
@updo.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    form = DataUploadForm()
    if request.method == 'POST':
        src_file = form.attach.data
        subdir = form.subdir.data
        sh = user_driven_connect()
        if sh:
            msg = sh.s3_upload(src_file, subdir, upload_fn='file')
            flash(msg)
        return redirect(url_for('.upload'))
    return render_template('./updown/uploader.html', form=form,
                           panel_args=dict(
                               patex='File upload to s3',
                               tadata='upload_tdata.html'
                           ))


@updo.route('/download')
@login_required
def download():
    # Row click activates detail for member
    if request.args:
        d_name = request.args.get('d')
        if d_name:
            sh = user_driven_connect()
            msg = sh.s3_delete(d_name)
            flash(msg)
        else:
            s_name = request.args.get('s')
            return redirect(url_for('.s3_downloader', s_name=s_name))
    # Presentation
    sh = user_driven_connect()
    if not sh: form = []
    else: form = sh.keys
    return render_template('panelbuilder.html',
                           form=form,
                           endpoint='.download',
                           panel_args=dict(
                               wid=8,
                               patex='Files for Download or Delete',
                               tadata='bucket_files_tdata.html'
                           ),
                           kwargs={}
                           )


@updo.route('/keyrotate')
@admin_required
def keyrotate():
    """
    interacts with s3 to create new keys (where possible)
    """
    kr = KeyRotation(AWS_KEYS['S3_KEY'], AWS_KEYS['S3_SECRET'])
    kr.rotate_keys()
    # delete old keys held on s3
    for un in kr.get_usernames():
        kr.terminate_oldkeys(un, make='del')
    # store the new keys on db
    for obj in kr.newKeyData:
        MemberBucketStore.create(**obj)
    return render_template('log_auth/home.html')


@updo.route('/keyremove')
@admin_required
def keyremove():
    """
    delete all older keys held on db;
    this should be a (visual - keeps table shorter) convenience function only.
    """
    for user_name, ct in Counter(x.user_name
                                 for x in MemberBucketStore.query).items():
        if ct > 1:
            rows = MemberBucketStore.query.filter_by(user_name=user_name).\
                order_by(desc(MemberBucketStore.id)).all()
            rows.pop(0)
            for row in rows:
                row.delete()
    return render_template('log_auth/home.html')


@updo.route('/adm_bucketmap', methods=['GET', 'POST'])
@admin_required
def adm_bucketmap():
    """
    We want to manually wire (for now) the member_id
    so that the login of the APP member is associated
    with the S3 member (called an IAM).

    That S3 member has been independently (and manually) created.
    """
    if request.method == 'POST':
        all_mem_ids = set(x.id for x in Member.query)
        for mid, bu, un, iam in zip(
                request.form.getlist('member_id'),
                request.form.getlist('bucket'),
                request.form.getlist('user_name'),
                MemberBucketStore.query.order_by(MemberBucketStore.id).all()
        ):
            iam.update(bucket=bu, user_name=un)
            if mid.isdigit() and int(mid) in all_mem_ids:
                iam.update(member_id=int(mid))
        return redirect(url_for('.adm_bucketmap'))
    # Presentation of existing data
    all_iams = []
    for iam in MemberBucketStore.query.order_by(MemberBucketStore.id).all():
        form = BucketMap()
        form.get_existing_data(iam)
        all_iams.append(form)
    if not all_iams:
        flash(f40)
        return redirect(url_for('log_auth.home'))
    # Presentation of existing members / Repetition from log_auth!
    all_members = Member.query.order_by(Member.id).all()
    return render_template(
            'panelbuilder.html',
            form=[all_iams, all_members],
            endpoint='.adm_bucketmap',
            panel_args=dict(
               wid=8,
               patex=current_app.config['PAHDS']['adm_bucketmap'],
               tadata=current_app.config['TADATA']['adm_bucketmap']
            ),
            kwargs={}
    )


"""
@updo.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    form = DataUploadForm()
    if request.method == 'POST':
        if form.bucket.data:
            bucket = conn_to_s3_bucket(form.bucket.data)
        else:
            bucket = conn_to_s3_bucket()
        src_file = form.attach
        subdir = form.subdir.data
        s3_upload(src_file, subdir, bucket)
        # src_file.data.save('./app/static/data/' + src_name)
        return redirect(url_for('.upload'))
    else:
        src_name = None
    return render_template('./updown/uploader.html', form=form,
                           panel_args=dict(
                               patex='File upload to s3',
                               tadata='upload_tdata.html'
                           ))
"""
"""
@updo.route('/download')
@login_required
def download():
    # Row click activates detail for member
    if request.args:
        d_name = request.args.get('d')
        if d_name:
            s3_delete(d_name)
        else:
            s_name = request.args.get('s')
            return redirect(url_for('.s3_downloader', s_name=s_name))
    # Presentation
    bucket = conn_to_s3_bucket()
    if not bucket: form = []
    else: form = bucket.list()
    return render_template('panelbuilder.html',
                           form=form,
                           endpoint='.download',
                           panel_args=dict(
                               wid=6,
                               patex='Files for Download or Delete',
                               tadata='bucket_files_tdata.html'
                           ),
                           kwargs={}
                           )
"""

# ==================================================
# @updo.route('/sumdata', methods=['GET', 'POST'])
# def sumdata_file():
#     form = DataUploadForm()
#     if request.method == 'POST':
#         return jsonify({"result": request.get_array(field_name='file')})
#     return render_template('./updown/sumdata.html', form=form)
#
# @updo.route('/download', methods=['GET'])
# @login_required
# def download_file():
#     return excel.make_response_from_array([[1,2], [3, 4]], "csv")

"""
def s3_conn_bucket(S3_KEY, S3_SECRET, bucket_name):
    # Connect to Amazon S3
    try:
        conn = boto.connect_s3(S3_KEY, S3_SECRET)
        return conn.get_bucket(bucket_name)
    except:
        flash(f170.format('access S3'))
"""
"""
def conn_to_s3_bucket(bucketname=AWS_BASE_DIR):  # bit of a fudge

    adapt connection approach based upon user;
    bucketname only matters for admins (who use a master key).

    # flash(AWS_KEYS['S3_KEY'])
    # flash(AWS_KEYS['S3_SECRET'])
    # flash(bucketname)
    if not current_user.adminr:
        try:
            row = MemberBucketStore.query.filter_by(member_id=current_user.id).\
                order_by(desc(MemberBucketStore.id)).first()
            return s3Handler(row.access_key_id, row.secret_access_key, row.bucket)
        except:  # if it has not been bucket-mapped, row returns empty
            flash(f170.format('access S3'))
            return None
    else:
        return s3Handler(AWS_KEYS['S3_KEY'], AWS_KEYS['S3_SECRET'], bucketname)
"""
"""
def s3_delete(key):
    try:
        bucket = conn_to_s3_bucket()
        bucket.delete_key(key)
        flash(f71.format(key))
    except:
        flash(f170.format('delete data'))
"""


"""
# Gets addressing because it uses the browser for downloading
@updo.route('/s3_downloader/<s_name>')
@login_required
def s3_downloader(s_name):
    try:
        bucket = conn_to_s3_bucket()
        key = bucket.get_key(s_name)
        # In-memory file save
        buffer = StringIO()
        key.get_contents_to_file(buffer)
        buffer.seek(0)
        flash(f72.format(s_name))
        return send_file(buffer, as_attachment=True, attachment_filename=s_name)
    except:
        flash(f170.format('download data'))
"""
