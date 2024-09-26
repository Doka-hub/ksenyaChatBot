from abc import ABCMeta
from importlib import import_module

from aiogram.handlers import BaseHandlerMixin, BaseHandler
from aiogram.fsm.context import FSMContext

from apps.users.models import TGUser
from apps.utils.keyboards.texts import BACK


class BaseStateMixin:
    @property
    def state(self) -> FSMContext:
        return self.data['state']


class BaseGetUserMixin:
    @property
    def user(self) -> TGUser:
        return self.data.get('user')


class StateHandlerMixin(BaseStateMixin, BaseHandlerMixin, metaclass=ABCMeta):
    pass


class GetUserHandlerMixin(BaseGetUserMixin, BaseHandlerMixin, metaclass=ABCMeta):
    pass


class BackHandlerMixin(BaseStateMixin, BaseHandlerMixin, metaclass=ABCMeta):
    back_str: str = BACK
    back_handler: BaseHandler | str = None

    def get_back_handler(self, back_handler: BaseHandler | str = None):
        if back_handler is None:
            back_handler = self.back_handler
        if isinstance(back_handler, str):
            module_name, class_name = back_handler.rsplit('.', 1)
            module = import_module(module_name)
            back_handler = getattr(module, class_name)
        return back_handler

    @property
    def is_back(self) -> bool:
        return self.event.text == self.back_str

    async def back(self, back_handler: BaseHandler | str = None):
        back_handler = self.get_back_handler(back_handler)
        return await back_handler(self.event, **self.data).handle()
