from aiogram.filters.callback_data import CallbackData


class PolicyConfirmCallbackData(CallbackData, prefix='policy'):
    confirm: bool = True
