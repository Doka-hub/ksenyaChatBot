from celery import Celery
from celery.schedules import crontab

from .loader import settings


celery_app = Celery('app', broker=settings.REDIS_URL, )
celery_app.autodiscover_tasks(
    [
        'apps.notifications.tasks',
    ],
)

celery_app.conf.update(TIMEZONE=settings.TIMEZONE)
celery_app.conf.beat_schedule = {
}
