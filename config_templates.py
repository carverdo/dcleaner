"""
The moving parts for templates.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'


class TemplateParameters(object):
    PAHDS = dict(
        addtasks = 'Build your schedule',
        adm_members = 'Control Default Settings of Members',
        curtasks = 'Your scheduled tasks',
        profile = 'Change your Password',
        signin = 'Get logged in to begin...',
        signup = 'Let\'s get you signed up...'
    )
    TADATA = dict(
        addtasks = 'timer_tdata.html',
        adm_members = 'adm_members_tdata.html',
        curtasks = 'sched_tdata.html',
        profile = 'profile_tdata.html',
        signin = 'signin_tdata.html',
        signup = 'signup_tdata.html'
    )
    PANEL = dict(PAHDS=PAHDS, TADATA=TADATA)
