from typing import List

from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ButtonType

from apps.utils.keyboards.texts import BACK


def get_keyboard(
    buttons_rows: List[List[ButtonType]],
    is_back_button: bool = False,
    back_button_name: str = BACK,
) -> ReplyKeyboardMarkup:

    builder = ReplyKeyboardBuilder()
    for buttons_row in buttons_rows:
        builder.row(*buttons_row, width=1)

    if is_back_button:
        builder.row(KeyboardButton(text=back_button_name))

    return builder.as_markup(resize_keyboard=True)


def get_back_keyboard(back_button_name: str = BACK) -> ReplyKeyboardMarkup:
    back_keyboard = get_keyboard(
        [
            [KeyboardButton(text=back_button_name)]
        ],
    )
    return back_keyboard
