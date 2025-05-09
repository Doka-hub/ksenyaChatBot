from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from .crud import TGUserCRUD


class GetUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user, created = await TGUserCRUD.get_or_create(user_id=str(event.from_user.id))

        # если пользователь заблокировал бота ранее, а потом разблокировал, даем доступ
        if user.is_bot_blocked:
            await TGUserCRUD.bot_unblock(user)

        user_data = {}
        for field in ['username', 'first_name', 'last_name']:
            if getattr(user, field) != getattr(event.from_user, field):
                user_data[field] = getattr(event.from_user, field)

        if user_data:
            await TGUserCRUD.update(user, **user_data)

        data['user'] = user
        return await handler(event, data)
