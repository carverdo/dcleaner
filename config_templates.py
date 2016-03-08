"""
The moving parts for templates.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'


class TemplateParameters(object):
    PAHDS = dict(
        # addtasks = 'Build your schedule',
        adm_members = 'Control Default Settings of Members',
        adm_visits = 'Member Visits (click on a row to expand)',
        adm_bucketmap = 'Allow bucket access: connect DB to S3',
        # balldata = 'Movement Data',
        # curtasks = 'Your scheduled tasks',
        profile = 'Change your Password',
        signin = 'Log in to begin...',
        signup = 'Sign up to get started',
        # str_amount = 'SOME WORDS'
    )
    TADATA = dict(
        # addtasks = 'xx_timer_tdata.html',
        adm_members = 'adm_members_tdata.html',
        adm_visits = 'adm_visits_tdata.html',
        adm_INDIvisits = 'adm_INDIvisits_tdata.html',
        adm_bucketmap = 'adm_bucketmap_tdata.html',
        # balldata = 'xx_device_tracker_tdata.html',
        # curtasks = 'xx_sched_tdata.html',
        profile = 'profile_tdata.html',
        signin = 'signin_tdata.html',
        signup = 'signup_tdata.html',
        # str_amount = 'xx_stramount_tdata.html'
    )
    PANEL = dict(PAHDS=PAHDS, TADATA=TADATA)
