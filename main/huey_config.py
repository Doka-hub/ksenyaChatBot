from huey import RedisHuey

from .loader import settings

# Инициализация Huey с Redis в качестве брокера
huey = RedisHuey(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

