from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage

from .settings import Settings

settings = Settings()
print(settings)
bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode='html'))
storage = RedisStorage.from_url(f'{settings.REDIS_HOST}:{settings.REDIS_PORT}')
dp = Dispatcher(storage=storage)
