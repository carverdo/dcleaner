__author__ = 'donal'
__project__ = 'dcleaner'
import os
import boto
from werkzeug import secure_filename
from uuid import uuid4
from config_vars import AWS_KEYS
from app.templates.flash_msg import *


class s3Handler(object):
    """
    Figure out who you are before calling.
    Exists as convenience function for all communications with AWS S3.
    """
    def __init__(self, S3_KEY, S3_SECRET, bucket_name):  # bit of a fudge
        self.key = S3_KEY
        self.secret = S3_SECRET
        self.bucket_name = bucket_name
        self.bucketconn = self.s3_conn_bucket()
        self.keys = list(self.bucketconn.list())

    def s3_conn_bucket(self):
        """Connect to Amazon S3."""
        try:
            conn = boto.connect_s3(self.key, self.secret)
            return conn.get_bucket(self.bucket_name)
        except:
            pass

    def s3_upload(self, src_address=None, upload_dir=None,
                  upload_fn='filename', str_data=None,
                  acl='authenticated-read'):
        dest_name = self._build_end_address(src_address, upload_dir)
        key = self.bucketconn.new_key(dest_name)
        # key.set_acl(acl)
        return self._run_key_function(src_address, upload_fn, str_data,
                                      dest_name, key)

    def s3_delete(self, key):
        try:
            self.bucketconn.delete_key(key)
            return f71.format(key)
        except:
            return f170.format('delete data')

    @staticmethod
    def _build_end_address(src_address, upload_dir):
        """
        :param src_address: full address
        :param upload_dir: subdireotory
        :return: address of endpoint
        """
        if isinstance(src_address, str):
            src_name = os.path.split(src_address)[1]
        else:
            src_name = secure_filename(src_address.filename)
        sta, dot_ext = os.path.splitext(src_name)
        dest_name = sta + '_' + uuid4().hex + dot_ext
        if upload_dir:
            dest_name = '/'.join([upload_dir, dest_name])
        return dest_name

    @staticmethod
    def _run_key_function(src_address, upload_fn, str_data,
                          dest_name, key):
        """
        :param src_address: either a string pointing to an address, a filename
            or a file
        :param upload_fn: we envisage three functions,
            from_string, from_file, from_filename
        :param str_data: None unless from_string
        :param dest_name: just for msging
        :param key: the endpoint
        :return: (uploads and) message
        """
        try:
            key_fn = getattr(key, 'set_contents_from_{}'.format(upload_fn))
            # handling the 'string' case
            if str_data: key_fn(str_data)
            else: key_fn(src_address)
            return f70.format(dest_name)
        except:
            return f170.format('upload data')


if __name__ == '__main__':
    print AWS_KEYS
    from config_project import EXCEL_BASE_DIR
    sh = s3Handler(AWS_KEYS['S3_KEY'], AWS_KEYS['S3_SECRET'], EXCEL_BASE_DIR)
    src_address = 'C:/Users/donal/downloads/small.txt'
    # load by 'filename'
    sh.s3_upload(src_address, 'smaller')
    # load by 'string'
    tmp = open(src_address).read()
    sh.s3_upload(src_address, 'smaller2', 'string', tmp)
    # load by 'file'
    # hard to do here

    """
    def s3_upload_by_filename(self, src_address, upload_dir=None,
                              acl='authenticated-read'):
        dest_name = self._build_end_address(src_address, upload_dir)
        key = self.bucketconn.new_key(dest_name)
        try:
            key.set_contents_from_filename(src_address)
            # flash(f70.format(dest_name))
            # key.set_acl(acl)
        except:
            # flash(f170.format('upload data'))
            pass

    def s3_upload_by_str(self, src_address, str_data, upload_dir=None,
                         acl='authenticated-read'):
        dest_name = self._build_end_address(src_address, upload_dir)
        key = self.bucketconn.new_key(dest_name)
        try:
            key.set_contents_from_string(str_data)
            # key.set_acl(acl)
            return f70.format(dest_name)
        except:

            return f170.format('upload data')
    """
    """
    def s3_upload_by_filename(src_address, upload_dir=None, acl='authenticated-read'):
    src_name = os.path.split(src_address)[1]
    sta, dot_ext = os.path.splitext(src_name)
    dest_name = sta + '_' + uuid4().hex + dot_ext
    if upload_dir:
        dest_name = '/'.join([upload_dir, dest_name])
    bucket = conn_to_s3_bucket(EXCEL_BASE_DIR)
    key = bucket.new_key(dest_name)
    try:
        key.set_contents_from_filename(src_address)
        flash(f70.format(dest_name))
        # key.set_acl(acl)
    except:
        flash(f170.format('upload data'))
    """

"""
def s3_upload_by_str(src_name, str_data, upload_dir=None, acl='authenticated-read'):
    src_name = os.path.split(src_name)[1]
    sta, dot_ext = os.path.splitext(src_name)
    dest_name = sta + '_' + uuid4().hex + dot_ext
    if upload_dir:
        dest_name = '/'.join([upload_dir, dest_name])
    bucket = conn_to_s3_bucket(EXCEL_BASE_DIR)
    key = bucket.new_key(dest_name)
    try:
        key.set_contents_from_string(str_data)
        flash(f70.format(dest_name))
        # key.set_acl(acl)
    except:
        flash(f170.format('upload data'))



@updo.route('/_s3_keys', methods=["GET", "POST"])
def _s3_keys():
    # Presentation
    # return conn_to_s3_bucket(EXCEL_BASE_DIR).list()
    return user_driven_connect().keys
"""
