from aiogram.filters.callback_data import CallbackData


class PaymentCallbackData(CallbackData, prefix='payment'):
    type: str


class PaymentApproveCallbackData(CallbackData, prefix='payment_approve'):
    name: str = 'yes'
