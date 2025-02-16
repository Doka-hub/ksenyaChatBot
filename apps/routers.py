from aiogram import F, Router
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER, IS_ADMIN
from aiogram.types import ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator

from .handlers.admins import DownloadExcelHandler
from .handlers.channels import ChannelJoinHandler, ChannelRequestHandler
from .handlers.start import StartHandler
from .users.filters import UserIsActive, UserIsManager
from .users.keyboards.texts import TO_MENU
from .utils.routers import (
    message_register,
    chat_join_request_register,
    chat_member_register,
)
from .utils.misc.bot_commands import DownloadExcelCommand

router = Router()

# start
message_register(router, StartHandler, CommandStart())
message_register(router, StartHandler, UserIsActive(), F.text == TO_MENU)

message_register(router, DownloadExcelHandler, UserIsManager(False), Command(DownloadExcelCommand))

# channel join
chat_member_register(
    router,
    ChannelJoinHandler,
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER),
)
chat_join_request_register(router, ChannelRequestHandler)

__all__ = ['router']
