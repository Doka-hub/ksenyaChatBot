from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


def get_inline_keyboard(buttons_rows: List[List[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for buttons_row in buttons_rows:
        builder.row(*buttons_row)
    return builder.as_markup()
