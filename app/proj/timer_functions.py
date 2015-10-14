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
from app.gunner import SendEmail


# ==================
# FUNCTIONS LIST
# ==================
def test_fn(*args, **kwargs):
    """
    args: does not matter
    kwargs: does not matter
    """
    print 'args: {}'.format(args), datetime.now()
    print 'kwargs: {}'.format(kwargs), datetime.now()


def send_email(*args, **kwargs):
    """
    args: (['email.com', 'email2.com'], email_title)
    kwargs: {'template': 'body_text'}
    OR
    kwargs: {'msgtype': 'ON', 'template': 'payment_request', 'amount': '5', 'day': 'Monday', 'payee': 'Pat'}
    """
    SendEmail(*args, **kwargs)


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