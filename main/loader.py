from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode

from .settings import Settings

settings = Settings()
bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
storage = RedisStorage.from_url(f'{settings.REDIS_HOST}:{settings.REDIS_PORT}')
dp = Dispatcher(storage=storage)
