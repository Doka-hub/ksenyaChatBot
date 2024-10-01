from datetime import timedelta
from typing import Any

from aiogram.exceptions import TelegramBadRequest
from aiogram.handlers import MessageHandlerCommandMixin

from apps.payments.keyboards.inline import get_payment_choose_inline_keyboard
from apps.users.keyboards.inline import get_manager_menu_inline_keyboard
from apps.users.utils import get_user_payments
from apps.utils.handlers import MessageHandler
from apps.utils.misc import set_manager_bot_commands
from apps.utils.start_message import get_start_message


class StartHandler(MessageHandlerCommandMixin, MessageHandler):
    """
    Запуск бота
    """

    async def handle(self) -> Any:
        await self.bot.send_chat_action(self.chat.id, 'typing')
        if self.user.is_manager:
            await set_manager_bot_commands(self.bot)
            await self.event.answer(
                'Меню менеджера',
                reply_markup=get_manager_menu_inline_keyboard(),
            )
            return

        user_payments = await get_user_payments(self.user)

        if len(user_payments) >= 1:
            last = user_payments[-1]
            await self.event.answer(
                f'Ваша подписка активна до: {(last.paid_at + timedelta(days=30)).date()}',
            )
        else:
            start_message = await get_start_message()
            payment_choose_inline_keyboard = get_payment_choose_inline_keyboard()

            if start_message.photo:
                action = self.event.answer_photo
                media = start_message.photo
            elif start_message.video:
                action = self.event.answer_video
                media = start_message.video
            else:
                action = self.event.answer
                media = None

            if media:
                try:
                    await action(
                        media,
                        caption=start_message.text,
                        reply_markup=payment_choose_inline_keyboard,
                    )
                except TelegramBadRequest:
                    await self.event.answer(
                        start_message.text,
                        reply_markup=payment_choose_inline_keyboard,
                    )
            else:
                await action(
                    start_message.text,
                    reply_markup=payment_choose_inline_keyboard,
                )

        await self.event.delete()
