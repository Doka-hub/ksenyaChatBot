from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
