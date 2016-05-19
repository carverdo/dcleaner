"""
The moving parts for templates.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'


class TemplateParameters(object):
    PAHDS = dict(
        adm_members = 'Control Default Settings of Members',
        adm_visits = 'Member Visits (click on a row to expand)',
        adm_bucketmap = 'Allow bucket access: connect DB to S3',
        profile = 'Change your Password',
        signin = 'Log in to begin...',
        signup = 'Sign up to get started',
        projset = 'Choose your Project'
    )
    TADATA = dict(
        adm_members = 'adm_members_tdata.html',
        adm_visits = 'adm_visits_tdata.html',
        adm_INDIvisits = 'adm_INDIvisits_tdata.html',
        adm_bucketmap = 'adm_bucketmap_tdata.html',
        profile = 'profile_tdata.html',
        signin = 'signin_tdata.html',
        signup = 'signup_tdata.html',
        projset = 'projset_tdata.html'
    )
    PANEL = dict(PAHDS=PAHDS, TADATA=TADATA)
