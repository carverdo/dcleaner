__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'


"""
# ===============================================
def send_simple_message(recip, subject, text):
    return requests.post(
        MAILGUN_URL.format(SANDBOX),
        auth=("api", MAILGUN_KEY),
        data={
            "from": "Circadian Activate <postmaster@{}>".format(SANDBOX),
            "to": recip,
            "subject": subject,
            "text": text
        }
    )

recip = ['donal.carville@gmail.com']  #, 'matt@circadian-capital.com']
subject = 'Test 2'
text = 'Some text; threaded'
# send_simple_message(recip, subject, text)
"""



"""
from threading import Thread

with tmp_app.app_context():
    mail.send(msg)



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message('xx',
                  sender='donal@circadian-capital.com',
                  recipients=['info@circadian-capital.com'])
    msg.body='these are some words'

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
"""


"""
import os
from flask.ext.mail import Mail, Message
from app import create_app

# LOAD UP A TEMP APP
tmp_app = create_app('development')

# CONFIGS FOR MAIL
tmp_app.config['MAIL_SERVER'] = 'smtp.gmail.com'
tmp_app.config['MAIL_PORT'] = 465
tmp_app.config['MAIL_USE_TLS'] = False
tmp_app.config['MAIL_USE_SSL'] = True
tmp_app.config['MAIL_USERNAME'] = 'info@circadian-capital.com'  # os.environ.get('MAIL_USERNAME')
tmp_app.config['MAIL_PASSWORD'] = 'PASSWORD'  # os.environ.get('MAIL_PASSWORD')

mail = Mail(tmp_app)

# SIMPLE TEST MESSAGE
msg = Message('xx',
              sender=tmp_app.config['MAIL_USERNAME'],
              recipients=['donal.carville@gmail.com']
              )
msg.body = 'these are some words'
mail.send(msg)
"""
