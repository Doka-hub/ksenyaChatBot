from datetime import datetime

from aiohttp import web
from aiohttp.web_response import json_response

from apps.notifications.tasks import task_payment_paid, task_payment_unpaid
from apps.payments.crud import PaymentCRUD
from apps.payments.models import PaymentType
from apps.utils import stripe
from main.loader import settings

payment_app = web.Application()


async def stripe_handle(request: web.Request):
    # getting Stripe's data
    payload = await request.text()
    sig_header = str(request.headers['Stripe-Signature'])

    # validate request and get event data
    event = stripe.get_webhook_construct_event(
        payload,
        sig_header,
        settings.STRIPE_CHECKOUT_COMPLETED_WEBHOOK_SECRET_KEY,
    )

    # looking for payment in db
    stripe_id = event.data.object.id
    payment = await PaymentCRUD.get_by_field('stripe_id', stripe_id)

    # mark payment paid and notify user, send invite link to join to the channel
    await PaymentCRUD.update(payment, is_paid=True, paid_at=datetime.now())
    await task_payment_paid(payment.id)

    return json_response()


async def stripe_payment_unpaid(request: web.Request):
    # getting Stripe's data
    payload = await request.text()
    sig_header = str(request.headers['Stripe-Signature'])

    # validate request and get event data
    event = stripe.get_webhook_construct_event(
        payload,
        sig_header,
        settings.STRIPE_CHECKOUT_EXPIRED_WEBHOOK_SECRET_KEY,
    )

    # looking for payment in db
    stripe_id = event.data.object.id
    payment = await PaymentCRUD.get(stripe_id=stripe_id, type=PaymentType.EU)

    # notify user to make payment
    await task_payment_unpaid(payment.user.user_id)

    return json_response()


async def rb_payment_paid(request: web.Request):
    """
    Mark RB payment paid from admin managers
    :param request:
    :return:
    """
    # data: {payment_id: int}
    data = await request.json()

    payment_id = data.get('payment_id')
    payment = await PaymentCRUD.get(id=payment_id)

    if payment:
        response = {'status': 'payment_verified'}
        status_code = 200

        # same as line 26
        await task_payment_paid(payment_id)
    else:
        response = {'status': 'payment_unverified'}
        status_code = 401
    return json_response(response, status=status_code)


payment_app.add_routes(
    [
        web.post('/rb-payment-paid', rb_payment_paid),
        web.post('/stripe-completed', stripe_handle),
        web.post('/stripe-expired', stripe_payment_unpaid),
    ],
)
