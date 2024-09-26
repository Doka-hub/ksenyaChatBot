from aiogram.filters import BaseFilter
from aiogram.types import Message

from .models import TGUser


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, user: TGUser | None = None, *args, **kwargs):
        if user:
            return user.is_admin
        return False


class IsRegistered(BaseFilter):
    def __init__(self, is_register: bool = True):
        self.is_register = is_register

    async def __call__(self, message: Message, user: TGUser | None = None, *args, **kwargs):
        if user:
            return user.is_register == self.is_register
        return False == self.is_register


class UserIsActive(BaseFilter):
    def __init__(self, is_active: bool = True):
        self.is_active = is_active

    async def __call__(self, message: Message, user: TGUser | None = None, *args, **kwargs):
        if user:
            return user.is_active == self.is_active
        return False == self.is_active
