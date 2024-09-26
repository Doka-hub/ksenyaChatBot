from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.utils.keyboards import get_inline_keyboard


def get_channel_link_inline_keyboard(url) -> InlineKeyboardMarkup:
    channel_link_inline_keyboard = get_inline_keyboard(
        [
            [
                InlineKeyboardButton(
                    text='Вступить в канал!',
                    url=url,
                ),
            ],
        ]
    )
    return channel_link_inline_keyboard
