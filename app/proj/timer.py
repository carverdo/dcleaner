__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
import random
from datetime import datetime, timedelta
from app import lg  # don't auto-delete: see below
from app import scheduler
import types
import timer_functions as mod  # import importlib
from ..db_models import MemberSchedule
from flask.ext.login import current_user


class genDiary(object):
    """
    Generates a series of timestamps (our diary) according to
    our inputs:
    sta_date = (YYYY, MM, DD)
    sta_time = (hh, mm)
    n = N minutes (OR cut into n random pieces)
    end = (hh, mm)
    """
    def __init__(self, sta=datetime.now(), end=None, n=2):
        self.sta = sta
        if not end:
            self.end = self.sta + timedelta(hours=1)
        else:
            self.end = end
        self.n = n
        self.times = self.gen_times_fix()
        # self.times = self.gen_times_rand()

    def gen_times_fix(self):
        """fixed intervals start to finish"""
        tmp, times = self.sta + timedelta(minutes=self.n), []
        while tmp < self.end:
            times.append(tmp)
            tmp += timedelta(minutes=self.n)
        return times

    def gen_times_rand(self):
        """n random times"""
        times = map(lambda x: self._random_time(), range(self.n))
        times.sort()
        return times

    def _random_time(self):
        tdelta = int((self.end-self.sta).total_seconds())
        return self.sta + timedelta(seconds=random.randint(0, tdelta))


class DiariseTasks(genDiary):
    """
    Schedules the running of a chosen task repeatedly
    in accordance with a diary/schedule we create.

    The choice of task comes from the import of timer_functions
    which we drop into a dictionary.
    """
    @classmethod
    def get_functions(cls):
        # mod = importlib.import_module(fn_module)
        try: cls.di_functions
        except:
            cls.di_functions = {obj:mod.__dict__.get(obj) for obj in dir(mod) if
                                isinstance(mod.__dict__.get(obj), types.FunctionType)
                                }
            # cls.mp = mod.Prevailer(**cls.di_functions)
        return cls.di_functions

    def __init__(self, *args, **kwargs):
        genDiary.__init__(self, *args, **kwargs)
        self.di_tasks = self.get_functions()
        self.ct = 0

    def run_tasks(self, task, *args, **kwargs):
        if not scheduler.running: scheduler.start()
        for t in self.times:
            scheduler.add_job(self.di_tasks[task],  #self.mp.__getattribute__(task),  #
                              trigger='date',
                              args=args, kwargs=kwargs,
                              id=str(self.ct),
                              name=task,
                              next_run_time=t,
                              jobstore='sqlalchemy' #'default' #
                              )
            MemberSchedule.create(member_id=current_user.id, task_id=self.ct)
            lg.logger.info("[{}] - added task to run at {}".format(datetime.now(), t))
            print "[{}] - added task to run at - {}".format(datetime.now(), t)
            self.ct = max(map(lambda x: int(x.id), self.remaining)) + 1

    # helper functions
    def get_remaining(self):
        return scheduler.get_jobs()
    remaining = property(get_remaining)

    def remaining_by_member(self):
        rel_tasks = [x.task_id for x in
                     MemberSchedule.query.filter(
                         MemberSchedule.member_id==current_user.id)
                     ]
        return filter(lambda r: int(r.id) in rel_tasks, self.remaining)
    remaining_by_member = property(remaining_by_member)

    def group_remaining(self):
        return set(x.name for x in self.remaining_by_member)

    def remove_group(self, name):
        """
        we used name to create subgroupings
        that we could later delete
        """
        del_ids = map(lambda x: x.id,
                      filter(lambda x: x.name == name, self.remaining)
                      )
        map(scheduler.remove_job, del_ids)

    def kill(self):
        """kills all future tasks"""
        scheduler.shutdown(wait=False)

    # ############
    def get_tasks(self):
        pass  # return self.scheduler.get_jobs()

    def pause(self):
        pass  # j.remove() single job only
        # for j in alta.scheduler.get_jobs(): print j.id, j


# ========================================
if __name__ == '__main__':
    """
    dt = DiariseTasks(
        end=datetime.strptime('2015-09-11 11:55:00', '%Y-%m-%d %H:%M:%S'),
        n=0.1)
    dt.run_tasks('test_fn', 'pop', a=2)
    dt.run_tasks('send_email',
                 'NAME@gmail.com',
                 'With timer',
                 None,
                 'A string of words.'
                 )
    """
