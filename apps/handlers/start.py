from typing import Any

from aiogram.exceptions import TelegramBadRequest
from aiogram.handlers import MessageHandlerCommandMixin
from aiogram.types import InlineKeyboardButton, KeyboardButton

from apps.payments.keyboards.inline import get_payment_choose_inline_keyboard
from apps.users.keyboards.inline import get_manager_menu_inline_keyboard
from apps.users.utils import get_user_active_subscriptions
from apps.utils.handlers import MessageHandler
from apps.utils.misc import set_manager_bot_commands
from apps.utils.start_message import get_start_message
from apps.utils.keyboards import get_inline_keyboard, get_keyboard


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
        else:
            subscriptions = await get_user_active_subscriptions(self.user)
            if subscriptions:
                last = subscriptions[-1]
                await self.event.answer(
                    f'Чао! Похоже, что Ваша подписка на Богемно -Нарядно все еще активна активна до: {last.active_by.strftime("%Y-%m-%d")}\nКе белло!'
                )
            else:
                start_message = await get_start_message()
                keyboards_data = start_message.buttons
                buttons = []
                for keyboard_data in keyboards_data:
                    if keyboard_data.type == 'INLINE':
                        buttons.append(
                            [
                                InlineKeyboardButton(
                                    text=keyboard_data.name,
                                    url=keyboard_data.url,
                                    callback_data=keyboard_data.callback_data,
                                ),
                            ],
                        )
                buttons = get_inline_keyboard(buttons)

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
                            reply_markup=buttons,
                        )
                    except TelegramBadRequest:
                        await self.event.answer(
                            start_message.text,
                            reply_markup=buttons,
                        )
                else:
                    await action(
                        start_message.text,
                        reply_markup=buttons,
                    )
