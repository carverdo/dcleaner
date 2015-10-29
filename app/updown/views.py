"""
Manage s3 uploads and downloads.
Not quite finished: tidy up the s3 defs and put into class.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from . import updo
from flask import render_template, request, flash, redirect, url_for, current_app
from flask.ext.login import current_user, login_required
from ..log_auth.views import admin_required
from forms import DataUploadForm, BucketMap
from werkzeug import secure_filename
from flask.ext import excel
from app.templates.flash_msg import *
import boto
import os
from uuid import uuid4
from sqlalchemy import desc
from collections import Counter
from config_vars import AWS_KEYS
from key_rotate import KeyRotation
from app.db_models import MemberBucketStore, Member


def s3_conn_bucket(S3_KEY, S3_SECRET, bucket_name):
    """Connect to Amazon S3."""
    try:
        conn = boto.connect_s3(S3_KEY, S3_SECRET)
        return conn.get_bucket(bucket_name)
    except:
        flash(f170.format('access S3'))


def run_naming(src_file):
    """
    Gens unique filename via uuid4.
    """
    src_name = secure_filename(src_file.data.filename)
    sta, dot_ext = os.path.splitext(src_name)
    return sta + uuid4().hex + dot_ext


def s3_upload(src_file, upload_dir=None, bucket=None, acl='authenticated-read'):
    """
    Uploads WTForm file object to given bucket.
    Access rights defaults to authenticated-read.
    SWITCHED OFF FOR NOW.
    """
    if bucket:
        dest_name = run_naming(src_file)
        if upload_dir:
            dest_name = '/'.join([upload_dir, dest_name])
        key = bucket.new_key(dest_name)
        try:
            key.set_contents_from_string(src_file.data.read())
            flash(f70.format(dest_name))
            # key.set_acl(acl)
        except:
            flash(f170.format('upload data'))
    else:
        pass


def s3_delete(bucket, key):
    try:
        bucket.delete_key(key)
        flash(f71.format(key))
    except:
        flash(f170.format('delete data'))


def s3_download(bucket, d_name):
    key = bucket.new_key(d_name)
    name_only = os.path.split(key.name)[-1]
    directory = os.path.join(os.environ['HOMEPATH'], 'downloads')
    if not os.path.exists(directory):
        os.makedirs(directory)
    key.get_contents_to_filename(os.path.join(directory, name_only))
    flash(f72.format(d_name))


# ==================================================
# @updo.route('/sumdata', methods=['GET', 'POST'])
# def sumdata_file():
#     form = DataUploadForm()
#     if request.method == 'POST':
#         return jsonify({"result": request.get_array(field_name='file')})
#     return render_template('./updown/sumdata.html', form=form)


def conn_to_s3_bucket(bucketname=None):
    """
    adapt connection approach based upon user;
    bucketname only matters for admins (who use a master key).
    """
    if not current_user.adminr:
        row = MemberBucketStore.query.filter_by(member_id=current_user.id).\
            order_by(desc(MemberBucketStore.id)).first()
        bucket = s3_conn_bucket(row.access_key_id, row.secret_access_key, row.bucket)
    else:
        bucket = s3_conn_bucket(AWS_KEYS['S3_KEY'], AWS_KEYS['S3_SECRET'], bucketname)
    return bucket


@updo.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    form = DataUploadForm()
    if request.method == 'POST':
        bucket = conn_to_s3_bucket(form.bucket.data)
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


@updo.route('/download')
@login_required
def download():
    if current_user.adminr:
        bucket = conn_to_s3_bucket('circadianboard')  # bit of a fudge
    else:
        bucket = conn_to_s3_bucket()
    # Row click activates detail for member
    if bucket and request.args:
        d_name = request.args.get('d')
        if d_name:
            s3_delete(bucket, d_name)
            return redirect(url_for('.download'))
        else:
            s_name = request.args.get('s')
            s3_download(bucket, s_name)
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


@updo.route('/download', methods=['GET'])
@login_required
def download_file():
    return excel.make_response_from_array([[1,2], [3, 4]], "csv")


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
    for user_name, ct in Counter(x.user_name for x in MemberBucketStore.query).items():
        if ct > 1:
            rows = MemberBucketStore.query.filter_by(user_name=user_name).\
                order_by(desc(MemberBucketStore.id)).all()
            rows.pop(0)
            for row in rows:
                row.delete()
    return render_template('log_auth/home.html')


@updo.route('/adm_bucketmap', methods=['GET', 'POST'])
def adm_bucketmap():
    """
    We want to manually wire (for now) the member_id
    so that the login of the APP member is associated
    with the S3 member (called an IAM).

    That S3 member has been independently (and manually)
    created.
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
            if mid.isdigit()and int(mid) in all_mem_ids:
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
    return render_template('panelbuilder.html',
                           form=all_iams,
                           endpoint='.adm_bucketmap',
                           panel_args=dict(
                               wid=8,
                               patex=current_app.config['PAHDS']['adm_bucketmap'],
                               tadata=current_app.config['TADATA']['adm_bucketmap']
                           ),
                           kwargs={}
                           )
