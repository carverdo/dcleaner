"""
This file's name ends up being included in the procfile against gunicorn.
If you change it, change there also.

The line if __name__ is important here. See favourites for explanation why.
Essentially, if missing gunicorn ends up running some other stuff it shouldn't.

Moved all the debug stuff to config.
"""
__author__ = 'donal'
__project__ = 'dcleaner'

from app import create_app
# app = create_app('development')
app = create_app('production')
if __name__ == '__main__':
    app.run()
