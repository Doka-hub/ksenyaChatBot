from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web_app import Application

from apps.users.middlewares import GetUserMiddleware
from apps.utils.middlewares import ThrottlingMiddleware


def create_app(bot, dp):
    app = Application()
    app["bot"] = bot

    SimpleRequestHandler(dp, bot, secret_token=bot.token).register(
        app,
        path=f'/tg/webhook',
    )
    setup_application(app, dp, bot=bot)
    return app


def create_bot(token):
    return Bot(token, default=DefaultBotProperties(parse_mode='html'))


def create_dispatcher(storage=None):
    if storage is None:
        storage = RedisStorage.from_url(f'redis://localhost:6379')
    return Dispatcher(storage=storage)

    # middlewares = register_middlewares(dp)
    # app = create_app(bot, dp, '')


def register_middlewares(dp):
    # Регистрация мидлварей
    dp.message.middleware.register(ThrottlingMiddleware())
    dp.message.outer_middleware.register(GetUserMiddleware())

    dp.callback_query.middleware.register(ThrottlingMiddleware())
    dp.callback_query.outer_middleware.register(GetUserMiddleware())

    dp.chat_join_request.middleware.register(ThrottlingMiddleware())
    dp.chat_join_request.outer_middleware.register(GetUserMiddleware())


def register_handlers(dp, router):
    # Подключение обработчиков
    dp.include_router(router)
