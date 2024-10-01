from typing import Any

from apps.channels.crud import ChannelCRUD
from apps.channels.keyboards.inline import get_channel_link_inline_keyboard
from apps.payments.keyboards.inline import get_payment_choose_inline_keyboard
from apps.users.utils import is_user_paid
from apps.utils.handlers import MessageHandler


class ChannelRequestHandler(MessageHandler):
    async def handle(self) -> Any:
        if await is_user_paid(self.user):
            user_joined = await self.event.bot.approve_chat_join_request(
                self.event.chat.id,
                self.from_user.id,
            )
            if user_joined:
                channel = await ChannelCRUD.get_first()
                await self.event.bot.send_message(
                    self.from_user.id,
                    'Ваша заявка принята!',
                    reply_markup=get_channel_link_inline_keyboard(channel.url),
                )
        else:
            await self.event.bot.approve_chat_join_request(self.event.chat.id, self.from_user.id, )
            await self.bot.send_message(
                self.from_user.id,
                'Для вступления в канал вам необходимо приобрести подписку!',
                reply_markup=get_payment_choose_inline_keyboard(),
            )
            await self.event.bot.ban_chat_member(self.event.chat.id, self.from_user.id)
            await self.event.bot.unban_chat_member(self.event.chat.id, self.from_user.id, True)
