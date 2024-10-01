from huey import RedisHuey

from .loader import settings

# Инициализация Huey с Redis в качестве брокера
huey = RedisHuey(url=settings.REDIS_URL)


from apps.notifications.tasks import *
