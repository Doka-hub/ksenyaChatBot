from datetime import datetime, timedelta

from apps.channels.crud import ChannelCRUD
from apps.channels.keyboards.inline import get_join_request_link_inline_keyboard
from apps.payments.crud import PaymentCRUD
from apps.payments.keyboards.inline import get_payment_choose_inline_keyboard
from apps.payments.models import Subscription
from apps.users.models import Role, TGUser
from main.celery import celery_app, celery_event_loop
from .utils import send_message


async def notify_managers(payment_id: int):
    payment = await PaymentCRUD.get_by_id(payment_id)
    managers = await TGUser.filter(TGUser.role == Role.manager.value).aio_execute()
    for manager in managers:
        await send_message(
            manager.user_id,
            message=f'Новый заказ! {payment.id}',
        )


@celery_app.task()
def task_notify_managers(payment_id: int):
    celery_event_loop.run_until_complete(notify_managers(payment_id))


async def payment_paid_notify(payment_id: int):
    payment = await PaymentCRUD.get_by_id(payment_id)
    channel = await ChannelCRUD.get_first()

    now = datetime.utcnow()
    active_by = now + timedelta(days=channel.duration)

    await PaymentCRUD.update(
        payment,
        is_paid=True,
        paid_at=now,
    )

    await Subscription.aio_create(
        payment=payment,
        user=payment.user,
        channel=channel,
        active_by=active_by,
    )

    await send_message(
        payment.user.user_id,
        message=f'Ваш заказ был оплачен! \nВот ваша ссылка для вступления - {channel.url}',
        reply_markup=get_join_request_link_inline_keyboard(channel.url),
    )
    task_update_subscription_notify.apply_async(
        (payment.id,),
        eta=datetime.utcnow() + timedelta(seconds=5)
    )


@celery_app.task()
def task_payment_paid_notify(payment_id: int):
    celery_event_loop.run_until_complete(payment_paid_notify(payment_id))


async def payment_unpaid_notify(user_id: int):
    await send_message(
        user_id,
        message=f'Вы не забыли оплатить заказ?',
        reply_markup=get_payment_choose_inline_keyboard(),
    )


@celery_app.task()
def task_payment_unpaid_notify(user_id: int):
    celery_event_loop.run_until_complete((payment_unpaid_notify(user_id))


async def update_subscription_notify(payment_id: int):
    payment = await PaymentCRUD.get_by_id(payment_id)
    user_id = payment.user.user_id

    await send_message(
        user_id,
        message=f'Ваша подписка подходит к концу ({payment.subscription.active_by})',
        reply_markup=get_payment_choose_inline_keyboard(),
    )


@celery_app.task()
def task_update_subscription_notify(payment_id: int):
    celery_event_loop.run_until_complete(update_subscription_notify(payment_id))
