import json

from aiohttp.client import ClientSession

from main.loader import storage
from .models import StartMessage

redis = storage.redis


async def save_message_data(key, message: StartMessage):
    serialized_message = message.json()
    await redis.setex(key, 60 * 60 * 72, serialized_message)  # 72 часа


async def get_start_message():
    start_message_data = await redis.get('start_message')

    if start_message_data:
        start_message = StartMessage(**json.loads(start_message_data))
    else:
        async with ClientSession() as client:
            response = await client.get('http://admin:8001/messages?type=greeter')
            data = await response.json()
            start_message = StartMessage(**data)
            await save_message_data('start_message', start_message)
    return start_message


async def get_after_subscribe_message():
    start_message_data = await redis.get('after_subscribe_message')

    if start_message_data:
        start_message = StartMessage(**json.loads(start_message_data))
    else:
        async with ClientSession() as client:
            response = await client.get('http://admin:8001/messages?type=after_subscribe')
            data = await response.json()
            start_message = StartMessage(**data)
            await save_message_data('after_subscribe_message', start_message)
    return start_message
