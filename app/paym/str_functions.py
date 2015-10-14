__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
from flask import flash
from app import stripe


def create_custo(r_form):
    """
    customer abstraction sits above any one-off payment (token)
    each new instantiation generates a unique customer.id at stripe
    along with any other form details.
    """
    return stripe.Customer.create(
        email=r_form['stripeEmail'],  # email submitted in form
        card=r_form['stripeToken']  # one-off token, mapping to credit card details
    )


def create_charge(customer, r_form):
    """
    we can now charge our customer's card;
    operates in similar fashion to customer.
    """
    try:
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(float(r_form['d_pounds']) * 100),
            currency=r_form['d_currency'],
            description=r_form['d_description'],
            metadata = {'my_codes': "0001"}  # personalisation
            )
    except stripe.error.CardError, e:
        flash('Card Declined')
        charge = None
    return charge
