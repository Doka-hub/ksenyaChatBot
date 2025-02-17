from pprint import pprint
from typing import Any

from aiogram.exceptions import TelegramForbiddenError

from apps.channels.crud import ChannelCRUD
from apps.channels.keyboards.inline import get_channel_link_inline_keyboard
from apps.payments.keyboards.inline import get_payment_choose_inline_keyboard
from apps.users.utils import have_user_active_subscription
from apps.utils.handlers import ChatMemberHandler, MessageHandler
from apps.utils.messages import get_after_subscribe_message


class ChannelJoinHandler(ChatMemberHandler):
    async def handle(self):
        pprint(self.event)
        pprint(self.from_user)
        invite_link = await self.event.bot.export_chat_invite_link(self.event.chat.id)
        invite_link = await self.event.bot.create_chat_invite_link(self.event.chat.id, member_limit=1)
        print(invite_link)
        message = await get_after_subscribe_message()
        if invite_link:
            try:
                await self.event.bot.send_message(
                    self.from_user.id,
                    message.text,
                    reply_markup=get_channel_link_inline_keyboard(invite_link),
                )
            except TelegramForbiddenError:
                pass


class ChannelRequestHandler(MessageHandler):
    async def handle(self) -> Any:
        if await have_user_active_subscription(self.user):
            user_joined = await self.event.bot.approve_chat_join_request(
                self.event.chat.id,
                self.from_user.id,
            )
            if user_joined:
                channel = await ChannelCRUD.get_first()
                await self.event.bot.send_message(
                    self.from_user.id,
                    'А перейти в сам канал можно кливнув по кнопке “Богемно-нарядно”. Кликайте и переходите в канал. Вьени куа: ',
                    reply_markup=get_channel_link_inline_keyboard(channel.url),
                )
        else:
            await self.event.bot.approve_chat_join_request(self.event.chat.id, self.from_user.id, )
            await self.bot.send_message(
                self.from_user.id,
                'Скуза! Похоже, что вы не приобрели подписку для вступления в канал.',
                reply_markup=get_payment_choose_inline_keyboard(),
            )
            await self.event.bot.ban_chat_member(self.event.chat.id, self.from_user.id)
            await self.event.bot.unban_chat_member(self.event.chat.id, self.from_user.id, True)
