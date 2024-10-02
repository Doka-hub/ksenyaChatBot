from datetime import timedelta
from io import BytesIO

from aiohttp import ClientSession
from aiohttp import FormData

from apps.channels.crud import ChannelCRUD
from apps.channels.models import Channel
from apps.payments.crud import PaymentCRUD
from apps.payments.models import Payment, PaymentType, Subscription
from apps.users.utils import have_user_subscription
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
        channel=channel,
    )
    return payment, payment_url


async def create_subscription(payment: Payment, channel: Channel):
    # если у пользователя уже есть подписка, то создаем новую подписку со сдвинутой датой
    if await have_user_subscription(payment.user):
        subscription = await Subscription.filter(
            Subscription.user == payment.user,
            Subscription.active_by <= payment.paid_at,
        ).aio_execute()
        active_by = subscription.active_by + timedelta(days=channel.duration)
    else:
        active_by = payment.paid_at + timedelta(days=channel.duration)

    subscription = await Subscription.aio_create(
        payment=payment,
        user=payment.user,
        channel=channel,
        active_by=active_by,
    )
    return subscription


async def send_screenshot(payment_id: int, screenshot, bot):
    file = await bot.get_file(screenshot.file_id)
    mime_type = file.file_path.split('.')[-1]

    bytesio = BytesIO()
    await bot.download(screenshot.file_id, bytesio)
    data = FormData()
    data.add_field(
        'screenshot',
        bytesio.read(),
        filename=f'screenshot.{mime_type}',
        content_type=f'image/{mime_type}',
    )

    async with ClientSession() as session:
        await session.post(
            f'http://admin:8001/payments/{payment_id}/upload-screenshot/',
            data=data,
        )
