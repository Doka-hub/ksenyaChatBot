from aiogram.filters.callback_data import CallbackData


class PaymentCallbackData(CallbackData, prefix='payment'):
    type: str
