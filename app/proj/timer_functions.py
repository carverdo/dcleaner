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
def do_nothing(*args, **kwargs):
    """
    args: does not matter
    kwargs: does not matter
    """
    pass


def test_fn(*args, **kwargs):
    print 'args: {}'.format(args), datetime.now()
    print 'kwargs: {}'.format(kwargs), datetime.now()


def send_email(*args, **kwargs):
    """
    args: (['email.com', 'email2.com'], email_title)
    kwargs: {'template':'body_text'}
    """
    SendEmail(*args, **kwargs)
