from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.utils.keyboards import get_inline_keyboard


def get_manager_menu_inline_keyboard() -> InlineKeyboardMarkup:
    manager_menu_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(
                    text='Оплачено!',
                    url='http://localhost:8001/admin/'
                ),
            ],
        ],
    )
    return manager_menu_inline_keyboard
