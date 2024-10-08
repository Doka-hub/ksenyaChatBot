from aiogram import Bot, Dispatcher
from aiogram.dispatcher.dispatcher import Update
from aiohttp import web
from aiohttp.web_response import json_response

from apps.chains.main import (
    create_bot,
)
from apps.routers import router
from apps.users.middlewares import GetUserMiddleware

add_bot_app = web.Application()


async def webhook(request: web.Request):
    data = await request.json()
    print(data)
    token = request.headers.get('X-Telegram-Bot-Api-Secret-Token', '')
    print(request.headers)
    print(token)
    bot = Bot('1961265445:AAFD1el6FHghZopASXplxR_LYQUXQYaq8rE')
    dp = Dispatcher()

    dp.message.outer_middleware.register(GetUserMiddleware())
    dp.callback_query.outer_middleware.register(GetUserMiddleware())
    dp.include_router(router)

    update = Update.model_validate(data, context={'bot': bot})
    await dp.feed_webhook_update(bot, update)
    await bot.session.close()
    del dp
    return json_response()


# todo сделать динамическое подключение роутеров
# как в сендпульс, добавляешь токен
# добавляешь тригеры, цепи
# как-то обновляешь обработчики
# посты от тг должны вызывать нужные обработчики
async def add_bot(request: web.Request):
    data = await request.json()
    token = data['token']

    bot = create_bot(token)
    data = await bot.get_webhook_info()
    print(data.url)
    if data.url != 'https://4c4e-46-251-196-167.ngrok-free.app/api/bot/webhook':
        await bot.set_webhook(
            'https://4c4e-46-251-196-167.ngrok-free.app/api/bot/webhook',
            secret_token='123',
        )
    dp = Dispatcher()
    await bot.session.close()

    return json_response()


async def close_bot(request: web.Request):
    data = await request.json()
    token = data['token']
    bot = create_bot(token)
    await bot.delete_webhook()
    return json_response()


add_bot_app.add_routes(
    [
        web.post('/add', add_bot),
        web.post('/webhook', webhook),
    ],
)
