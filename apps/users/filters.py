from aiogram.filters import BaseFilter
from aiogram.types import Message

from .models import TGUser


class UserIsManager(BaseFilter):
    def __init__(self, value: bool = True):
        self.value = value

    async def __call__(self, message: Message, user: TGUser | None = None, *args, **kwargs):
        if user:
            return user.is_manager == self.value
        return False


class UserIsActive(BaseFilter):
    def __init__(self, value: bool = True):
        self.value = value

    async def __call__(self, message: Message, user: TGUser | None = None, *args, **kwargs):
        if user:
            return user.is_active == self.value
        return False == self.value
