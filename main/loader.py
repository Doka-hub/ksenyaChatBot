from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from .settings import Settings


class CustomDispatcher(Dispatcher):
    async def feed_update(self, bot, update, *args, **kwargs):
        print(update.event)
        print(update.event_type)
        return await super(CustomDispatcher, self).feed_update(bot, update, *args, **kwargs)


settings = Settings()
bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
storage = RedisStorage.from_url(f'{settings.REDIS_HOST}:{settings.REDIS_PORT}')
dp = CustomDispatcher(storage=storage)
