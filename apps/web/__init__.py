from aiohttp import web

from .payments import payment_app
from .utils import utils_app
from .add_bot import add_bot_app

web_app = web.Application()
web_app.add_subapp('/payments', payment_app)
web_app.add_subapp('/utils', utils_app)
web_app.add_subapp('/bot', add_bot_app)

__all__ = ['web_app']
