from apps.channels.crud import ChannelCRUD
from apps.payments.crud import PaymentCRUD
from apps.payments.models import Payment, PaymentType
from apps.utils import stripe


async def create_payment(user, payment_type) -> tuple[Payment, str | None]:
    channel = await ChannelCRUD.get_first()
    stripe_id = None
    amount = 0
    payment_url = None

    match PaymentType(payment_type):
        case PaymentType.EU:
            session = stripe.create_checkout_session(
                channel.eur_amount,
                payment_type,
                1,
                'payment',
                email=user.email,
            )
            amount = channel.eur_amount
            payment_url = session.url
            stripe_id = session.id
        case PaymentType.RB:
            amount = channel.rub_amount

    payment = await PaymentCRUD.create(
        user=user,
        stripe_id=stripe_id,
        amount=amount,
        type=payment_type,
    )
    return payment, payment_url
