from aiohttp.client import ClientSession

from main.celery import celery_app


@celery_app.task(bind=True, max_retries=5, default_retry_delay=300)
async def task_save_screenshot(self, payment_id: int, file_url: str):
    async with ClientSession() as client:
        response = await client.get(file_url)
        file_bytes = await response.read()

        response = await client.post(
            'https://google.com', data={
                'payment_id': str(payment_id),
                'file_bytes': file_bytes,
            },
        )
        if response.status != 200:
            return self.retry()
