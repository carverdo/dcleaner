__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()

from app.proj import timer_functions as mod
import types

di_functions = {obj:mod.__dict__.get(obj) for obj in dir(mod) if
                isinstance(mod.__dict__.get(obj), types.FunctionType)
                                }
mp = mod.Prevailer(**di_functions)
#### NEED TO FIGURE OUT HOW THIS SLOTS INTO TIMER   ####
### RMBR ONLY ADD CLS TO SOME TIMER_FUNCTIONS

sta = datetime.now()
for r in range(0,50,5):
    t = sta + timedelta(seconds=r)
    scheduler.add_job(mp.__getattribute__('page_render'), #   di_functions['blah'],
                      trigger='date',
                      args=('http://www.bbc.co.uk',), #, kwargs={'x': r},
                      next_run_time=t,
                      )
