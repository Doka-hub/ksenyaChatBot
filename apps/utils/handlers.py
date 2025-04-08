from abc import ABCMeta

from aiogram.filters.callback_data import CallbackData
from aiogram.handlers import (
    MessageHandler as AOMessageHandler,
    CallbackQueryHandler as AOCallbackQueryHandler,
    ChatMemberHandler as AOChatMemberHandler,
)

from .mixins import (
    StateHandlerMixin,
    GetUserHandlerMixin,
    BackHandlerMixin,
)


class MessageHandler(
    StateHandlerMixin,
    GetUserHandlerMixin,
    BackHandlerMixin,
    AOMessageHandler,
    metaclass=ABCMeta,
):
    pass


class ChatMemberHandler(
    StateHandlerMixin,
    GetUserHandlerMixin,
    BackHandlerMixin,
    AOChatMemberHandler,
    metaclass=ABCMeta,
):
    pass


class CallbackQueryHandler(
    StateHandlerMixin,
    GetUserHandlerMixin,
    AOCallbackQueryHandler,
    metaclass=ABCMeta,
):
    callback_class = CallbackData

    @property
    def parsed_callback_data(self):
        """
        Возвращает unpacked дату
        :return:
        """
        return self.callback_class.unpack(self.callback_data)
