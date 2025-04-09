from datetime import datetime

from apps.channels.crud import ChannelCRUD
from apps.channels.keyboards.inline import get_join_request_link_inline_keyboard
from apps.notifications.schemas import NotifyUsers
from apps.payments.crud import PaymentCRUD
from apps.payments.keyboards.inline import get_payment_choose_inline_keyboard
from apps.payments.models import Subscription
from apps.payments.utils import create_subscription
from apps.users.models import Role, TGUser
from main.celery import celery_app, celery_event_loop
from main.loader import bot
from .utils import send_message


async def notify_managers(payment_id: int):
    payment = await PaymentCRUD.get_by_id(payment_id)
    managers = await TGUser.filter(TGUser.role == Role.manager.value).aio_execute()
    message = f'''
<b>Новый заказ</b>:\n <a href="https://bot.chertovich.com/admin/payments/payment/{payment.id}/change/">Посмотреть</a>
'''
    for manager in managers:
        await send_message(
            manager.user_id,
            message=message,
        )


@celery_app.task()
def task_notify_managers(payment_id: int):
    celery_event_loop.run_until_complete(notify_managers(payment_id))


async def payment_paid_notify(payment_id: int):
    payment = await PaymentCRUD.get_by_id(payment_id)
    channel = await ChannelCRUD.get_first()

    now = datetime.utcnow()
    await PaymentCRUD.update(
        payment,
        is_paid=True,
        paid_at=now,
    )

    subscription = await create_subscription(payment, channel)

    await send_message(
        payment.user.user_id,
        message=f'Аллора, Ваш заказ был оплачен! Конгратулацьони!  Это ваша <a href="{channel.url}">ссылка</a> для вступления (нажмите на ссылку и кликните “запросить вступление”) так вы автоматически добавитесь в канал.',
        reply_markup=get_join_request_link_inline_keyboard(channel.url),
    )
    task_remove_user_from_channel.apply_async(
        (subscription.id,),
        eta=subscription.active_by,
    )


@celery_app.task()
def task_payment_paid_notify(payment_id: int):
    celery_event_loop.run_until_complete(payment_paid_notify(payment_id))


async def payment_unpaid_notify(user_id: int):
    await send_message(
        user_id,
        message=f'Скуза! Похоже, что вы еще раздумываете стоит ли присоединиться к каналу.  Будет очень жаль, не увидеть вас в Богемно-Нарядно! Это очень дорогой мне проект в который я вкладываю много любви, поверьте, он того стоит. Андиамо?',
        reply_markup=get_payment_choose_inline_keyboard(),
    )


@celery_app.task()
def task_payment_unpaid_notify(user_id: int):
    celery_event_loop.run_until_complete(payment_unpaid_notify(user_id))


async def remove_user_from_channel(subscription_id: int):
    subscription = await Subscription.aio_get(Subscription.id == subscription_id)
    user_id = subscription.user.user_id
    channel_id = subscription.channel.telegram_chat_id

    await bot.ban_chat_member(channel_id, user_id)
    await bot.unban_chat_member(channel_id, user_id)


@celery_app.task()
def task_remove_user_from_channel(subscription_id: int):
    celery_event_loop.run_until_complete(remove_user_from_channel(subscription_id))


async def notify(notify_users_data):
    data = {}
    notify_users_data = NotifyUsers(**notify_users_data)

    notification_id = notify_users_data.notification_id
    message = notify_users_data.message

    for user_id, tg_user_id in notify_users_data.users_ids:
        sent = await send_message(tg_user_id, message=message)
        if sent:
            now = datetime.now()
            data[int(user_id)] = now


@celery_app.task()
def task_notify(notify_users_data: dict):
    celery_event_loop.run_until_complete(notify(notify_users_data))
