from typing import ClassVar
from enum import Enum
from pathlib import Path

from pydantic import validator, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = '.env.local'

    class DBEngines(str, Enum):
        POSTGRESQL = 'postgresql'
        MYSQL = 'mysql'

    # BASE
    TIMEZONE: str
    ADMINS_IDS: list[int] = []
    MANAGERS_IDS: list[int] = []

    THROTTLE_TIME: ClassVar = 1

    # STRIPE
    STRIPE_SECRET_KEY: str
    STRIPE_CHECKOUT_SESSION_WEBHOOK_SECRET_KEY: str

    # WEB
    BASE_HOST: str = 'localhost'

    WEBHOOK_HOST: str = ''
    WEBHOOK_PATH: str = '/tg/webhook/'
    WEBHOOK_URL: str = None

    # BOT
    BOT_TOKEN: str
    BOT_USERNAME: str

    DEFAULT_FLAGS: ClassVar = {"throttling_key": "default"}

    # DATABASE
    DB_ENGINE: DBEngines = DBEngines.MYSQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str = 'redis://localhost'
    REDIS_PORT: int = 6379
    REDIS_URL: str = None

    # PATH
    BASE_DIR: ClassVar = Path(__file__).parent.parent
    APPS_DIR: ClassVar = BASE_DIR / 'apps'
    MIGRATIONS_FILE: ClassVar = BASE_DIR / 'migrations.json'
    MEDIA_DIR: ClassVar = BASE_DIR / 'media'
    LOGS_BASE_PATH: ClassVar = str(BASE_DIR / 'logs')

    @field_validator('WEBHOOK_URL', mode='before')
    @classmethod
    def set_webhook_url(cls, value, values):
        data = values.data
        WEBHOOK_HOST = data.get('WEBHOOK_HOST')
        WEBHOOK_PATH = data.get('WEBHOOK_PATH')
        return f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

    @field_validator('REDIS_URL', mode='before')
    @classmethod
    def set_redis_url(cls, value, values):
        data = values.data
        REDIS_HOST = data.get('REDIS_HOST')
        REDIS_PORT = data.get('REDIS_PORT')
        return f'{REDIS_HOST}:{REDIS_PORT}/'
