from aiohttp import web
from aiohttp.web_response import json_response

from apps.utils.start_message import save_start_message_data
from apps.utils.start_message.models import StartMessage

utils_app = web.Application()


async def save_start_message(request: web.Request):
    print(request)
    data = await request.json()
    await save_start_message_data(StartMessage(**data))
    return json_response()


utils_app.add_routes(
    [
        web.post('/start-message', save_start_message),
    ],
)
