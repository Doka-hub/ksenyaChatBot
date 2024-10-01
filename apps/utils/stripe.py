from decimal import Decimal

import stripe

from main.loader import settings

_stripe = stripe
_stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(
    amount: float | Decimal,
    currency: str,
    quantity: int,
    name: str,
    metadata=None,
    **kwargs,
) -> stripe.checkout.Session:
    session = _stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': name
                    },
                    'unit_amount': int(amount * 100),
                },
                'quantity': quantity,
            }
        ],
        mode='payment',
        success_url='https://t.me/web_app_testBot',
        metadata=metadata,
        customer_email=kwargs.get('email'),
    )
    return session


def get_webhook_construct_event(
    payload: dict,
    sig_header: str,
    endpoint_secret_key: str,
):
    try:
        event = _stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret_key,
        )
    except ValueError as e:
        # Invalid payload
        raise e
    return event
