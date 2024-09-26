from typing import Callable, Any

from aiogram import Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import State
from aiogram.handlers.base import BaseHandler

from main.loader import settings


def decorator(func):
    def wrapper(
        router,
        handler,
        *filters,
        flags=None,
        include_default_flags=True,
        states=None,
        **kwargs,
    ):
        state_filters = []
        if states:
            for state in states:
                state_filters.append(StateFilter(state))

        if state_filters:
            filters = (*filters, *state_filters)

        if flags is None:
            flags = {}

        if include_default_flags:
            flags = settings.DEFAULT_FLAGS.update(**flags)

        return func(
            router,
            handler,
            *filters,
            flags=flags,
            include_default_flags=include_default_flags,
            states=states,
            **kwargs,
        )

    return wrapper


@decorator
def chat_join_request_register(
    router: Router,
    handler: type(BaseHandler),
    *filters: Callable[..., Any],
    flags: dict[str, Any] | None = None,
    include_default_flags: bool = True,
    states: list[State] | None = None,
    **kwargs,
):
    router.chat_join_request.register(handler, *filters, flags=flags, **kwargs)


@decorator
def message_register(
    router: Router,
    handler: type(BaseHandler),
    *filters: Callable[..., Any],
    flags: dict[str, Any] | None = None,
    include_default_flags: bool = True,
    states: list[State] | None = None,
    **kwargs
):
    router.message.register(handler, *filters, flags=flags, **kwargs)


@decorator
def callback_query_register(
    router: Router,
    handler: type(BaseHandler),
    *filters: Callable[..., Any],
    flags: dict[str, Any] | None = None,
    include_default_flags: bool = True,
    states: list[State] | None = None,
    **kwargs
):
    router.callback_query.register(handler, *filters, flags=flags, **kwargs)
