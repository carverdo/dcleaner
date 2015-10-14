__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask.ext.wtf import Form  # Seems odd (this line not next) but correct: wtf Form is slightly different
from wtforms import StringField, FloatField


class StripeForm(Form):
    # d_name = StringField("d_name")  # cant see where this tracks to
    d_description = StringField("d_description")
    d_currency = StringField("d_currency", default="gbp")
    d_pounds = FloatField("d_amount", default=0.50)
