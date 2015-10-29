"""

"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask.ext.wtf import Form  # Seems odd (this line not next) but correct: wtf Form is slightly different
from wtforms import FileField, StringField, IntegerField


class DataUploadForm(Form):
    attach = FileField('Your data.')
    subdir = StringField("Subdirectory")
    bucket = StringField("Bucket")


class BucketMap(Form):
    """
    """
    member_id = IntegerField()
    bucket = StringField("Bucket")
    user_name = StringField("S3 Username")

    def get_existing_data(self, iam):
        # user-entry data
        self.member_id.default = iam.member_id
        self.bucket.default = iam.bucket
        self.user_name.default = iam.user_name
        # process those changes
        self.process()
