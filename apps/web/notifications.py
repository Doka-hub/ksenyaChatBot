from aiohttp import web
from aiohttp.web_response import json_response

from apps.notifications.schemas import NotificationType, NotifyUsers
from apps.notifications.tasks import task_notify

notifications_app = web.Application()


async def handle(request: web.Request):
    data = await request.json()
    notification_type = NotificationType.get_type(data['type'])

    post_data = {}
    task = None

    if notification_type == NotificationType.DEFAULT:
        post_data = NotifyUsers(**data).dict()
        task = task_notify
    print(data)
    task.delay(post_data)

    return json_response({'status': 'OK'})


notifications_app.add_routes(
    [web.post('/', handle)],
)
