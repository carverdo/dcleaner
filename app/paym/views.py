"""
With blueprints we can create a second area for view production because
views is independent of 'app'; when app is created it binds to the views.

Use this area to build out the particular project.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from . import paym
from flask import render_template, flash, redirect, url_for, request, current_app
from forms import StripeForm
from config_vars import STRIPE_KEYS
from app.paym.str_functions import create_custo, create_charge


@paym.route('/stramount', methods=['GET', 'POST'])
def stramount():
    form = StripeForm()
    if request.method == 'POST':
        endpoint = '.strcpt'
        kwargs = dict(**request.form)
        return redirect(url_for(endpoint, **kwargs))
    else:
        patex = current_app.config['PAHDS']['str_amount']
        tadata = current_app.config['TADATA']['str_amount']
        endpoint, kwargs = '', {}
        stripedata = dict(
            p_key=STRIPE_KEYS['publishable_key'],
            currency=form.data.get('d_currency')
        )
    return render_template('panelbuilder.html',
                           form=form,
                           endpoint=endpoint,
                           panel_args=dict(
                               patex=patex,
                               tadata=tadata,
                               stripedata=stripedata
                           ),
                           kwargs=kwargs
                           )


@paym.route('/strcpt', methods=['GET', 'POST'])
def strcpt():
    customer = create_custo(request.args)
    charge = create_charge(customer, request.args)
    flash(customer)
    flash(charge)
    return render_template('./paym/str_charge.html', amount=charge.amount)
