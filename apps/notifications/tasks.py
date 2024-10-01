from apps.channels.crud import ChannelCRUD
from apps.channels.keyboards.inline import get_join_request_link_inline_keyboard
from apps.payments.crud import PaymentCRUD
from apps.payments.keyboards.inline import get_payment_choose_inline_keyboard
from apps.users.models import Role, TGUser

from main.celery import celery_app
from .utils import send_message


@celery_app.task()
async def task_notify_managers(payment_id: int):
    payment = await PaymentCRUD.get_by_id(payment_id)
    managers = await TGUser.filter(TGUser.role == Role.manager.value).aio_execute()
    for manager in managers:
        await send_message(
            manager.user_id,
            message=f'Новый заказ! {payment.id}',
        )


@celery_app.task()
async def task_payment_paid(payment_id: int):
    payment = await PaymentCRUD.get_by_id(payment_id)
    channel = await ChannelCRUD.get_first()

    await send_message(
        payment.user.user_id,
        message=f'Ваш заказ был оплачен! \nВот ваша ссылка для вступления - {channel.url}',
        reply_markup=get_join_request_link_inline_keyboard(channel.url),
    )


@celery_app.task()
async def task_payment_unpaid(user_id: int):
    await send_message(
        user_id,
        message=f'Вы не забыли оплатить заказ?',
        reply_markup=get_payment_choose_inline_keyboard(),
    )
