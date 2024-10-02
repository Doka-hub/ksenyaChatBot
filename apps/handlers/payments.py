from typing import Any

from aiogram.types import ReplyKeyboardRemove

from apps.notifications.tasks import task_notify_managers
from apps.payments.callbacks import PaymentCallbackData, PaymentApproveCallbackData
from apps.payments.crud import RBDetailsCRUD
from apps.payments.keyboards.inline import get_approve_payment_inline_keyboard
from apps.payments.states import ChoosePaymentState, PaymentApproveState
from apps.payments.text_templates import rb_payment_details_text
from apps.payments.utils import create_payment, send_screenshot
from apps.users.crud import TGUserCRUD
from apps.users.utils import is_valid_email
from apps.utils.handlers import MessageHandler, CallbackQueryHandler
from apps.utils.keyboards.default import get_back_keyboard
from .start import StartHandler


class ChoosePaymentHandler(CallbackQueryHandler):
    callback_class = PaymentCallbackData

    async def handle(self) -> Any:
        payment_type = self.parsed_callback_data.type
        await self.state.update_data(payment_type=payment_type)

        # if user doesn't have an email
        if self.user.email is None:
            message = 'Введите вашу почту:'
            reply_markup = get_back_keyboard('Отменить')

            await self.state.set_state(ChoosePaymentState.email)
        else:
            reply_markup = ReplyKeyboardRemove()

            payment, payment_url = await create_payment(self.user, payment_type)
            await self.state.update_data(payment_id=payment.id)

            if payment_url:
                message = f'''Вот ваша ссылка на оплату: <a href="{payment_url}">клик</a>'''
            else:
                rb_details = await RBDetailsCRUD.get_first()
                message = rb_payment_details_text.format(
                    account_number=rb_details.account_number,
                    field_1=rb_details.field_1,
                    field_2=rb_details.field_2,
                )
                reply_markup = get_approve_payment_inline_keyboard()
                await self.state.set_state(PaymentApproveState.paid)

        await self.event.message.answer(message, reply_markup=reply_markup)


class EmailHandler(MessageHandler):
    back_str = 'Отменить'
    back_handler = StartHandler
    callback_class = PaymentCallbackData

    async def handle(self) -> Any:
        if self.is_back:
            await self.state.clear()
            return await self.back()

        email = self.event.text
        if is_valid_email(email):
            message = await self.event.answer('Обрабатываем...', reply_markup=ReplyKeyboardRemove())
            await message.delete()

            await TGUserCRUD.update(self.user, email=self.event.text)

            state_data = await self.state.get_data()
            payment_type = state_data.get('payment_type')

            payment, payment_url = await create_payment(self.user, payment_type)

            if payment_url:
                message = f'''Вот ваша ссылка на оплату: <a href="{payment_url}">клик</a>'''
                reply_markup = None
            else:
                rb_details = await RBDetailsCRUD.get_first()
                message = rb_payment_details_text.format(
                    account_number=rb_details.account_number,
                    field_1=rb_details.field_1,
                    field_2=rb_details.field_2,
                )
                reply_markup = get_approve_payment_inline_keyboard()
                await self.state.set_state(PaymentApproveState.paid)

            await self.state.update_data(payment_id=payment.id)
        else:
            reply_markup = None
            message = 'Введите правильную почту'

        await self.event.answer(message, reply_markup=reply_markup)


class PaymentApproveHandler(CallbackQueryHandler):
    callback_class = PaymentApproveCallbackData

    async def handle(self) -> Any:
        await self.event.message.answer(
            'Мы почти закончили! Отправьте пожалуйста скриншот перевода, чтобы мы могли подтвердить ваш платеж!',
        )
        await self.state.set_state(PaymentApproveState.screenshot)


class ScreenshotHandler(MessageHandler):
    async def handle(self) -> Any:
        state_data = await self.state.get_data()
        payment_id = state_data['payment_id']

        # photo getting and link creation to next send to admin service
        screenshot = self.event.photo[-1]

        await send_screenshot(payment_id, screenshot, self.bot)
        await self.event.answer(
            f'Супер! Наши менеджеры скоро проверят ваш платеж и одобрят вам доступ к каналу!'
        )
        await self.state.clear()

        task_notify_managers.delay(payment_id)
