from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import ContentType

from .handlers.admins import DownloadExcelHandler
from .handlers.channels import ChannelRequestHandler
from .handlers.payments import (
    ChoosePaymentHandler,
    EmailHandler,
    PaymentApproveHandler,
    ScreenshotHandler,
)
from .handlers.start import StartHandler
from .payments.callbacks import PaymentCallbackData, PaymentApproveCallbackData
from .payments.states import ChoosePaymentState, PaymentApproveState
from .users.filters import UserIsActive, UserIsManager
from .users.keyboards.texts import TO_MENU
from .utils.routers import (
    callback_query_register,
    message_register,
    chat_join_request_register,
)
from .utils.misc.bot_commands import DownloadExcelCommand

router = Router()

# start
message_register(router, StartHandler, UserIsActive(), CommandStart())
message_register(router, StartHandler, UserIsActive(), F.text == TO_MENU)

# payment
callback_query_register(
    router,
    ChoosePaymentHandler,
    PaymentCallbackData.filter(),
)
message_register(router, EmailHandler, states=[ChoosePaymentState.email])
callback_query_register(
    router,
    PaymentApproveHandler,
    PaymentApproveCallbackData.filter(),
    states=[PaymentApproveState.paid],
)
message_register(
    router,
    ScreenshotHandler,
    F.content_type.is_(ContentType.PHOTO),
    states=[PaymentApproveState.screenshot],
)

message_register(router, DownloadExcelHandler, UserIsManager(False), Command(DownloadExcelCommand))

# channel join
chat_join_request_register(router, ChannelRequestHandler)

__all__ = ['router']
