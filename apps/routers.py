from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import ContentType

from .handlers.admins import DownloadExcelHandler
from .handlers.channels import ChannelJoinHandler, ChannelRequestHandler
from .handlers.payments import (
    ChoosePaymentHandler,
    EmailHandler,
    PaymentApproveHandler,
    ScreenshotHandler,
)
from .handlers.policy import PolicyConfirmHandler
from .handlers.start import StartHandler
from .payments.callbacks import PaymentCallbackData, PaymentApproveCallbackData
from .payments.states import ChoosePaymentState, PaymentApproveState
from .users.filters import UserIsActive, UserIsManager
from .users.callbacks import PolicyConfirmCallbackData
from .users.keyboards.texts import TO_MENU
from .utils.routers import (
    callback_query_register,
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
)
chat_join_request_register(router, ChannelRequestHandler)

__all__ = ['router']
