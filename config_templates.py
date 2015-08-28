"""
The moving parts for templates.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'


class TemplateParameters(object):
    PAHDS = dict(
        signup = "Let's get you signed up...",
        signin = 'Get logged in to begin...',
        profile = 'Change your Password'
        )
    TADATA = dict(
        signup = 'signup_tdata.html',
        signin = 'signin_tdata.html',
        profile = 'profile_tdata.html'
        )
    PANEL = dict(PAHDS=PAHDS, TADATA=TADATA)
