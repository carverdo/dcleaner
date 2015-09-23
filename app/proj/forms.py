"""

"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'

from flask.ext.wtf import Form  # Seems odd (this line not next) but correct: wtf Form is slightly different
from wtforms import StringField, DateTimeField, FloatField, SelectField, TextAreaField
from datetime import datetime, timedelta
import ast
from .timer import DiariseTasks


# ==========================
# TIMER
# ==========================
class TimerForm(Form, DiariseTasks):
    starter = DateTimeField('sta') #, default=datetime.now())
    ender = DateTimeField("end") #, default=datetime.now() + timedelta(minutes=10))
    ner = FloatField(default=0.5)
    task = SelectField('TasktoRun', choices=[(x, x) for x in
                                             DiariseTasks.get_functions().keys()]
    )
    args = TextAreaField(default=(['donal.carville@gmail.com'], 'Rugby Game', 5.0, 'Friday'))  # default="enter your args here... 14, 'fixed',")
    kwargs = TextAreaField(default={'aa': 0})  # default="and your kwargs here... {'a':1, 'b':2}")

    @classmethod
    def get_args(cls):
        # the important stuff
        cls.get_functions()
        # the rest is just for grabbing __doc__
        # text and pretty printing
        try: cls.di_args
        except:
            cleaner = lambda text: None if text is None else \
                [ele.strip() for ele in text.strip().split('\n')]
            cls.di_args = {k:cleaner(v.__doc__) for k, v
                           in cls.di_functions.items()}
            cls.printof_args = []
            for k, v in cls.di_args.items():
                cls.printof_args.append(k)
                if isinstance(v, list):
                    for ele in v: cls.printof_args.append(ele)
                cls.printof_args.append('---------------')
        return cls.printof_args

    def update_vals(self):
        self.starter.data = datetime.now()
        self.ender.data = datetime.now() + timedelta(seconds=55)
        #self.process()

    def run_task(self):
        """build schedule and run function accordingly"""
        try:
            DiariseTasks.__init__(self, sta=self.starter.data,
                                  end=self.ender.data, n=self.ner.data)
            self.run_tasks(self.task.data,
                           *ast.literal_eval(self.args.data),
                           **ast.literal_eval(self.kwargs.data)
                           )
            self.run_taskFail = False
        except:
            self.run_taskFail = True
