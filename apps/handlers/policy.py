from typing import Any

from aiogram.types import ReplyKeyboardRemove

from apps.payments.crud import RBDetailsCRUD
from apps.payments.keyboards.inline import get_approve_payment_inline_keyboard
from apps.payments.states import ChoosePaymentState, PaymentApproveState
from apps.payments.utils import create_payment
from apps.users.callbacks import PolicyConfirmCallbackData
from apps.users.crud import TGUserCRUD
from apps.utils.handlers import CallbackQueryHandler
from apps.utils.keyboards.default import get_back_keyboard


class PolicyConfirmHandler(CallbackQueryHandler):
    callback_class = PolicyConfirmCallbackData

    async def handle(self) -> Any:
        await TGUserCRUD.update(self.user, **{'policy_confirmed': True})
        data = await self.state.get_data()
        payment_type = data['payment_type']
        await self.event.answer('Подтверждено')

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

        await self.event.message.answer(message, reply_markup=reply_markup)
