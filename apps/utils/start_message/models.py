import pydantic
from aiogram.types import InlineKeyboardButton, KeyboardButton


class ButtonMessage(pydantic.BaseModel):
    type: str['INLINE' | 'KEYBOARD']
    name: str
    url: str | None = None
    callback_data: str | None = None


class StartMessage(pydantic.BaseModel):
    text: str
    photo: str | None = None
    video: str | None = None
    buttons: list[ButtonMessage] | None = None
