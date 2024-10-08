from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.users.callbacks import PolicyConfirmCallbackData
from apps.utils.keyboards import get_inline_keyboard


def get_manager_menu_inline_keyboard() -> InlineKeyboardMarkup:
    manager_menu_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(
                    text='Админка',
                    url='https://bot.chertovich.com/admin/'
                ),
            ],
        ],
    )
    return manager_menu_inline_keyboard


def get_policy_confirm_inline_keyboard() -> InlineKeyboardMarkup:
    manager_menu_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(
                    text='Ва бене, согласен!',
                    callback_data=PolicyConfirmCallbackData().pack(),
                ),
            ],
        ],
    )
    return manager_menu_inline_keyboard
