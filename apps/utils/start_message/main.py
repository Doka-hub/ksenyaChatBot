import json

from aiohttp.client import ClientSession

from main.loader import storage
from .models import StartMessage

redis = storage.redis


async def save_start_message_data(message: StartMessage):
    serialized_message = message.json()
    await redis.setex('start_message', 3600, serialized_message)


async def get_start_message():
    start_message_data = await redis.get('start_message')

    if start_message_data:
        start_message = StartMessage(**json.loads(start_message_data))
    else:
        async with ClientSession() as client:
            response = await client.get('http://admin:8001/start-message/')
            data = await response.json()
            print(data)
            start_message = StartMessage(**data)
            await save_start_message_data(start_message)
    return start_message
