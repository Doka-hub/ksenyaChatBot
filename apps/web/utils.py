from aiohttp import web
from aiohttp.web_response import json_response

from apps.utils.messages import save_message_data
from apps.utils.messages.models import StartMessage

utils_app = web.Application()


async def save_message(request: web.Request):
    data = await request.json()
    message_type = data.get('type')
    await save_message_data(message_type, StartMessage(**data))
    return json_response()


utils_app.add_routes(
    [
        web.post('/messages', save_message),
    ],
)
