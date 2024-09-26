from aiohttp import web

from .payments import payment_app
from .utils import utils_app

web_app = web.Application()
web_app.add_subapp('/payments', payment_app)
web_app.add_subapp('/utils', utils_app)

__all__ = ['web_app']
