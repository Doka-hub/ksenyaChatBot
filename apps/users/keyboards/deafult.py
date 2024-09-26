from aiogram.types import KeyboardButton, WebAppInfo

from apps.utils.keyboards.default import get_keyboard


def get_manager_menu_keyboard():
    return get_keyboard(
        [
            [
                KeyboardButton(
                    text='Админка',
                    web_app=WebAppInfo(url='http://localhost:8001/admin/'),
                ),
            ]
        ]
    )
