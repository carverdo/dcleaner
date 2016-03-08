__author__ = 'donal'
__project__ = 'dcleaner'

import requests
from threading import Thread
from flask import render_template
from config_vars import MAILGUN_URL, SANDBOX, MAILGUN_KEY


class SendEmail(object):
    fr = "Circadian Activate <postmaster@{}>".format(SANDBOX)

    def __init__(self, *args, **kwargs):
        self.data = {}
        self.build_message(*args, **kwargs)
        self.send_email()

    def build_message(self, recip, subject, msgtype=None, template=None,
                      **kwargs):
        self.data = {
            "from": self.fr,
            "to": recip,
            "subject": subject
        }
        # we either have html messages or text-only messages
        if msgtype is not None:
            try:
                # our preference: building real html pages
                temp_text = render_template('./guns/{}.html'.format(
                        template), **kwargs)
            except:
                # fallback: string populating with html formatting
                # needed with the scheduler
                temp_text = open('./app/templates/guns/{}.txt'.format(
                        template)).read()
                temp_text = temp_text.format(**kwargs)
            self.data["html"] = temp_text
        else:
            self.data["text"] = template

    @staticmethod
    def send_async_email(data):
        requests.post(
            MAILGUN_URL.format(SANDBOX),
            auth=("api", MAILGUN_KEY),
            data=data
        )

    def send_email(self):
        thr = Thread(target=self.send_async_email, args=[self.data])
        thr.start()
        return thr


# ==========================================
if __name__ == '__main__':
    SendEmail(
        ['NAME@gmail.com'],
        'Some Title Words',
        template='This is where the text goes.'
    )
    # we have not here tested the template version (gets tested in views.py)
