from typing import List, Iterable

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web_app import Application

from apps.routers import router
from apps.users.middlewares import GetUserMiddleware
from apps.utils.middlewares import ThrottlingMiddleware
from apps.utils.misc import logging
from apps.web import web_app
from .loader import settings, bot, dp


async def on_startup(webhook_url):
    old_webhook_url = await bot.get_webhook_info()
    allowed_updates = [
        'message',
        'edited_message',
        'channel_post',
        'edited_channel_post',
        'callback_query',
        'inline_query',
        'chosen_inline_result',
        'shipping_query',
        'pre_checkout_query',
        'poll',
        'poll_answer',
        'my_chat_member',
        'chat_member',
    ]
    print(old_webhook_url.url, webhook_url)
    print(old_webhook_url.allowed_updates, allowed_updates)
    if old_webhook_url.url != webhook_url or old_webhook_url.allowed_updates != allowed_updates:
        await bot.delete_webhook(True)
        await bot.set_webhook(
            webhook_url,
            allowed_updates=allowed_updates,
        )
    else:
        print(f'Webhook already set {webhook_url}')

    # # Установка команд для бота
    # print(444)


def bot_setup():
    logging.setup()
    print('Bot setup')

    dp['webhook_url'] = settings.WEBHOOK_URL
    dp.startup.register(on_startup)

    # Регистрация мидлварей
    dp.message.middleware.register(ThrottlingMiddleware())
    dp.message.outer_middleware.register(GetUserMiddleware())

    dp.callback_query.middleware.register(ThrottlingMiddleware())
    dp.callback_query.outer_middleware.register(GetUserMiddleware())

    dp.chat_join_request.middleware.register(ThrottlingMiddleware())
    dp.chat_join_request.outer_middleware.register(GetUserMiddleware())

    # Подключение обработчиков
    dp.include_router(router)


def create_app():
    bot_setup()
    print('123')

    app = Application()
    app["bot"] = bot

    subapps: List[Iterable[str, Application]] = [
        # здесь добавляем свои веб-приложения (например админка)
        ('/api', web_app),
    ]

    #    app.router.add_static('/bot-static', 'static')
    for prefix, subapp in subapps:
        subapp['bot'] = bot
        subapp['dp'] = dp
        app.add_subapp(prefix, subapp)

    SimpleRequestHandler(
        dp,
        bot,
        # secret_token=settings.BOT_TOKEN,
    ).register(
        app,
        path='/tg/webhook/',
    )
    setup_application(app, dp, bot=bot)
    return app
