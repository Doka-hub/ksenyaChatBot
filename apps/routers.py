from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import ContentType

from apps.payments.callbacks import PaymentCallbackData, PaymentApproveCallbackData
from apps.users.filters import UserIsActive
from apps.users.keyboards.texts import TO_MENU
from apps.utils.routers import (
    callback_query_register,
    message_register,
    chat_join_request_register,
)
from .handlers.channels import ChannelRequestHandler
from .handlers.payments import (
    ChoosePaymentHandler,
    EmailHandler,
    PaymentApproveHandler,
    ScreenshotHandler,
)
from .handlers.start import StartHandler
from .payments.states import ChoosePaymentState, PaymentApproveState

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

# channel join
chat_join_request_register(router, ChannelRequestHandler)

__all__ = ['router']
