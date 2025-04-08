from typing import Any

from aiogram.types import ReplyKeyboardRemove

from apps.notifications.tasks import task_notify_managers
from apps.payments.callbacks import PaymentCallbackData, PaymentApproveCallbackData
from apps.payments.crud import RBDetailsCRUD
from apps.payments.keyboards.inline import get_approve_payment_inline_keyboard
from apps.payments.states import ChoosePaymentState, PaymentApproveState
from apps.payments.utils import create_payment, send_screenshot
from apps.users.crud import TGUserCRUD
from apps.users.keyboards.inline import get_policy_confirm_inline_keyboard
from apps.users.utils import is_valid_email
from apps.utils.handlers import MessageHandler, CallbackQueryHandler
from apps.utils.keyboards.default import get_back_keyboard
from .start import StartHandler


class ChoosePaymentHandler(CallbackQueryHandler):
    callback_class = PaymentCallbackData

    async def handle(self) -> Any:
        payment_type = self.parsed_callback_data.type
        await self.state.update_data(payment_type=payment_type)

        if self.user.policy_confirmed:
            # if user doesn't have an email
            if self.user.email is None:
                message = 'Введите пожалуйста свою почту, рагацци'
                reply_markup = get_back_keyboard('Отменить')

                await self.state.set_state(ChoosePaymentState.email)
            else:
                reply_markup = ReplyKeyboardRemove()

                payment, payment_url = await create_payment(self.user, payment_type)
                await self.state.update_data(payment_id=payment.id)

                if payment_url:
                    message = f'Грацие милле! Для оплаты перейдите пожалуйста по <a href="{payment_url}">ссылке</a> '
                else:
                    rb_details = await RBDetailsCRUD.get_first()
                    message = rb_details.text
                    reply_markup = get_approve_payment_inline_keyboard()
                    await self.state.set_state(PaymentApproveState.paid)
        else:
            message = 'Грацие! Переходя к следующему шагу вы подтверждаете, что согласны с договором <a href="https://docs.google.com/document/d/e/2PACX-1vTgQ5QbEIqgJMwo2IBVw7Xk5YRSItI6yTO0mos7yxGdP1Tt_VOJPCDWV0P_FRxJS7qVBVOyY65aNVO4/pub">публичной офертой</a>'
            reply_markup = get_policy_confirm_inline_keyboard()
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
                message = f'Грацие милле! Для оплаты перейдите пожалуйста по <a href="{payment_url}">ссылке</a> '
                reply_markup = None
            else:
                rb_details = await RBDetailsCRUD.get_first()
                message = rb_details.text

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
            'Мольто бене! Мы почти закончили! Отправьте пожалуйста скриншот перевода, чтобы мы могли подтвердить ваш платеж!',
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
            'Перфетто! Наш менеджер проверит ваш платеж и в скором времени одобрит ваш доступ к каналу!'
        )
        await self.state.clear()

        task_notify_managers.delay(payment_id)
