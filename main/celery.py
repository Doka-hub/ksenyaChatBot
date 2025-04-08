import asyncio

from celery import Celery

from .loader import settings

celery_app = Celery('app', broker=settings.REDIS_URL, )
celery_app.autodiscover_tasks(
    [
        'apps.notifications.tasks',
    ],
)

celery_event_loop = asyncio.new_event_loop()

celery_app.conf.update(TIMEZONE=settings.TIMEZONE)
celery_app.conf.beat_schedule = {
}
