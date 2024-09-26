from typing import Any

from aiogram.types import (
    ChatMemberLeft,
    ChatMemberRestricted,
    ChatMemberBanned,
)

from apps.users.utils import is_user_paid
from apps.utils.handlers import MessageHandler


class ChannelRequestHandler(MessageHandler):
    async def handle(self) -> Any:
        print(self.user)
        if await is_user_paid(self.user):
            chat_member = await self.event.bot.get_chat_member(
                self.event.chat.id,
                self.from_user.id,
            )
            print(chat_member.status)
            # if chat_member.status in [ChatMemberLeft, ChatMemberRestricted, ChatMemberBanned]:
            await self.event.bot.approve_chat_join_request(
                self.event.chat.id,
                self.from_user.id,
            )
        else:
            await self.event.bot.approve_chat_join_request(self.event.chat.id, self.from_user.id, )
            await self.bot.send_message(
                self.from_user.id,
                'Для вступления в канал вам необходимо приобрести подписку!',
            )
            await self.event.bot.ban_chat_member(self.event.chat.id, self.from_user.id)
            await self.event.bot.unban_chat_member(self.event.chat.id, self.from_user.id, True)
