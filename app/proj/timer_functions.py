"""
DONT CHANGE THIS MODULE'S NAME.

Drop any classes or functions here that we
might want to run on the scheduler.

We DONT especially want you defining functions here,
but that will work too.

The group of functions then gets compiled elsewhere for presentation
to the user.

The __doc__ string is shown on screen.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from datetime import datetime
from app.gunner import SendEmail, SendEmail2
from app.proj.url_grab.simple import PageRender
# from flask.ext.login import current_user

# ==================
# FUNCTIONS LIST
# ==================
"""
def do_nothing(*args, **kwargs):

    args: does not matter
    kwargs: does not matter

    pass


def test_fn(*args, **kwargs):
    print 'args: {}'.format(args), datetime.now()
    print 'kwargs: {}'.format(kwargs), datetime.now()

"""

def send_email(*args, **kwargs):
    """
    args: (['email.com', 'email2.com'], email_title)
    kwargs: {'template':'body_text'}
    """
    SendEmail(*args, **kwargs)


def request_payment(*args, **kwargs):
    """
    args: (['phone.com'], 'Message')
    kwargs: {'amount_gbp':'5.00'}
    """
    SendEmail2(*args, msgtype='on', template='payment_request', **kwargs)


# ==================
# TESTING fns for CLASS WRAPPER
# ==================
"""
def page_render(cls, *args, **kwargs):

    args: ('http://www.bbc.co.uk')
    kwargs: none

    pr = PageRender(*args, **kwargs)
    with open('pare.txt', 'a') as fil:
        fil.write(pr.text + '\n')
    cls.prevailing = pr.text


def blah(cls, *args, **kwargs):
    cls.prevailing = kwargs['x']**2
"""

# ==================
# CLASS WRAPPER
# ==================
class Prevailer(object):
    """
    This is a wrapper over the functions from timer_functions.
    It allows us to store a prevailing result from any run of a function.
    This is useful as we run through schedules of jobs.
    """
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self.__class__, k, v)