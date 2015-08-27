__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from config_vars import MAILGUN_URL, SANDBOX, MAILGUN_KEY
import requests
from threading import Thread
from flask import render_template


def build_message(recip, subject, template, **kwargs):
    return {
        "from": "Circadian Activate <postmaster@{}>".format(SANDBOX),
        "to": recip,
        "subject": subject,
        "html": render_template(template + '.txt', **kwargs)
        }


def send_async_email(data):
    requests.post(
        MAILGUN_URL.format(SANDBOX),
        auth=("api", MAILGUN_KEY),
        data=data
    )


def send_email(*args, **kwargs):
    data = build_message(*args, **kwargs)
    thr = Thread(target=send_async_email, args=[data])
    thr.start()
    return thr


if __name__ == '__main__':
    recip = ['donal.carville@gmail.com']  #, 'matt@circadian-capital.com']
    subject = 'Test Yikes'
    text = 'Some text; threaded, testing imports'
    # kwargs = {'user.username': 'dony', }
    # send_email(recip, subject, './templates/confirm_body', **kwargs)
    # data = build_message(recip, subject, text)
