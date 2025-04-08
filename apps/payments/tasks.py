from aiohttp import ClientSession

from main.celery import celery_app, celery_event_loop


async def send_screenshot(payment_id: int, data):
    async with ClientSession() as session:
        await session.post(
            f'http://admin:8001/payments/{payment_id}/upload-screenshot/',
            data=data,
        )


@celery_app.task()
def task_send_screenshot(payment_id: int, data):
    celery_event_loop.run_until_complete(send_screenshot(payment_id, data))
