from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.payments.callbacks import PaymentCallbackData, PaymentApproveCallbackData
from apps.payments.models import PaymentType
from apps.utils.keyboards import get_inline_keyboard


def get_payment_choose_inline_keyboard() -> InlineKeyboardMarkup:
    payment_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(
                    text='Оплатить в ЕС',
                    callback_data=PaymentCallbackData(type=PaymentType.EU).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Оплатить в РБ',
                    callback_data=PaymentCallbackData(type=PaymentType.RB).pack(),
                ),
            ],
        ],
    )
    return payment_inline_keyboard


def get_approve_payment_inline_keyboard() -> InlineKeyboardMarkup:
    payment_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(
                    text='Оплачено!',
                    callback_data=PaymentApproveCallbackData().pack(),
                ),
            ],
        ],
    )
    return payment_inline_keyboard
