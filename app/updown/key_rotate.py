"""
KEY ROTATION
As a safety device you want to be able to kill all existing keys and replace with new ones.

TO DO:
1. Crude on the Donal exclude (as mainuser); better if any S3 with admin rights is auto-excluded.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
import boto

class KeyRotation(object):
    """
    Runs key rotation.
    Populates newKeyData indicating that:
        1. a connection was made;
        2. a newkey was able to be created (not always true); and
        3. the previous/old keys were set to Inactive.

    If newKeyData indicates that no new key  could be created,
    the previously existing final key remains unchanged.

    Although not explicitly intertwined, this also does a bucket lookup
    to try and guess the bucket associated with each user.
    """
    def __init__(self, S3_KEY, S3_SECRET):
        self.S3_KEY = S3_KEY
        self.S3_SECRET = S3_SECRET
        self.bucket_map, self.newKeyData = {}, []
        self.isconnected = False
        # try a connection
        self.iam_conn = self.iam_conn_bucket()

    def rotate_keys(self):
        """Generate new, kill old"""
        if self.isconnected:
            self.guess_buckets()
            for user_name in self.get_usernames():
                newKeyData = self.create_newkey(user_name)
                newKeyData = self.add_bucket_guess(newKeyData, user_name)
                self.newKeyData.append(newKeyData)
                self.terminate_oldkeys(user_name)

    def guess_buckets(self):
        """
        Assumes one statement per bucket (which may have multi-user_names;
        add also then, that any user_name shows up in only one bucket.
        """
        for bucket in boto.connect_s3(self.S3_KEY, self.S3_SECRET).get_all_buckets():
            try:
                aws_strings = eval(bucket.get_policy())['Statement'][0]['Principal']['AWS']
                if isinstance(aws_strings, list):
                    for aws_string in aws_strings:
                        print aws_string.split('/')[-1]
                        print bucket.name
                        self.bucket_map[aws_string.split('/')[-1]] = bucket.name
                else:
                    print aws_strings.split('/')[-1]
                    print bucket.name
                    self.bucket_map[aws_strings.split('/')[-1]] = bucket.name
            except:
                pass

    def add_bucket_guess(self, tmp, user_name):
        try:
            tmp['bucket'] = self.bucket_map[user_name]
        except:
            pass
        return tmp

    def iam_conn_bucket(self):
        """Connect to Amazon IAM."""
        try:
            conn = boto.connect_iam(self.S3_KEY, self.S3_SECRET)
            self.isconnected = True
            return conn
        except:
            pass

    def get_usernames(self):
        """convenience fn."""
        all_users = self.iam_conn.get_all_users()['list_users_response']['list_users_result']['users']
        all_users = map(lambda x: x['user_name'], all_users)
        return self._strike_mainuser(all_users)

    @staticmethod
    def _strike_mainuser(all_users, mainuser='Donal'):
        """
        For convenience don't change the credentials of the original authorising party of the class itself.
        Do this manually.
        """
        return filter(lambda x: x != mainuser, all_users)

    def create_newkey(self, username):
        """
        You are only allowed two keys per user, so this will
        occasionally error out.
        """
        try:
            return self.iam_conn.create_access_key(username)\
                ['create_access_key_response']['create_access_key_result'][u'access_key']
        except:
            pass

    def terminate_oldkeys(self, username, make='Inactive'):
        """Either make inactive or kill users' allButLast keys."""
        userKeyData = self.iam_conn.get_all_access_keys(username)\
            ['list_access_keys_response']['list_access_keys_result']['access_key_metadata']
        userKeyData.sort(key=lambda x: x['create_date'])
        for ouk in userKeyData[:-1]:  # ignore the final (new) key
            aki = ouk['access_key_id']
            # make inactive
            if make == 'Inactive':
                if ouk['status'] == 'Active':
                    self.iam_conn.update_access_key(aki, 'Inactive', username)
            # OR, delete
            else:
                self.iam_conn.delete_access_key(aki, username)


# ==========================
if __name__ == '__main__':
    import os
    aws_keys = os.environ.get('AWS_KEYS').split(' ')
    kr = KeyRotation(aws_keys[0], aws_keys[1])
    kr.guess_buckets()
    """
    kr.rotate_keys()
    # this is optional
    for un in kr.get_usernames():
        kr.terminate_oldkeys(un, make='irrel')
    """