from asyncio import sleep

from aiogram.exceptions import (
    TelegramForbiddenError,
    TelegramRetryAfter,
    TelegramUnauthorizedError,
    TelegramBadRequest,
)
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InputFile
from loguru import logger

from apps.notifications.crud import UsersNotificationsCRUD
from apps.notifications.models import UsersNotifications
from apps.users.crud import TGUserCRUD
from main.loader import bot


def make_text(title: str, text: str) -> str:
    return f'*{title or ""}*' + '\n\n' + f'{text or ""}'


async def send_message(
    to: str | int,
    title: str | None = None,
    text: str | None = None,
    message: str | None = None,
    image_id: str | None = None,
    video_id: str | None = None,
    document: InputFile = None,
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None,
    disable_notification: bool = False,
    tries: int = 0,
    max_tries: int = 5,
) -> bool:
    """
    :param to: user_id
    :param title:
    :param text:
    :param message:
    :param image_id:
    :param video_id:
    :param document:
    :param reply_markup:
    :param disable_notification: отключаем звук
    :param tries: `n` совершенные попытки
    :param max_tries: пробуем отправить сообщение максимум `n` раз
    :return:
    """
    if tries == max_tries - 2:
        await sleep(60)
    elif tries == max_tries - 1:
        await sleep(60)
    elif tries >= max_tries:
        return False

    # лимиты телеграма 30 сообщений в секунду
    await sleep(.05)

    logger.info('sending to: {to}', to=to)

    try:
        if not message:
            message = make_text(title, text)

        if image_id:
            await bot.send_media_group(
                to,
                image_id,
                caption=message,
                reply_markup=reply_markup,
                disable_notification=disable_notification,
            )
        elif video_id:
            await bot.send_video(
                to,
                video_id,
                caption=message,
                reply_markup=reply_markup,
                disable_notification=disable_notification,
            )
        elif document:
            await bot.send_document(
                to,
                document,
                reply_markup=reply_markup,
                disable_notification=disable_notification,
            )
        else:
            await bot.send_message(
                to,
                message,
                reply_markup=reply_markup,
                disable_notification=disable_notification,
            )
        return True

    except TelegramRetryAfter as e:
        await sleep(float(e.retry_after))
        return await send_message(
            to,
            title,
            text,
            message,
            image_id,
            video_id,
            document,
            reply_markup,
            disable_notification,
            tries + 1,
            max_tries,
        )
    except TelegramForbiddenError as e:
        if e.message.endswith('bot was blocked by the user'):
            await TGUserCRUD.bot_block(to)
        logger.info('TelegramForbiddenError: {e}', e=e)
    except TelegramUnauthorizedError as e:
        logger.info('TelegramUnauthorizedError: {e}', e=e)
    except TelegramBadRequest as e:
        logger.info('TelegramBadRequest: {e}', e=e)
    return False


async def notify_statistic(notification_id: int, data: dict):
    delivered_users_ids = list(data.keys())

    users_notifications: list[UsersNotifications] = await UsersNotificationsCRUD.list(
        UsersNotifications.notification_id == notification_id,
        UsersNotifications.user_id.in_(delivered_users_ids),
    )
    for user_notification in users_notifications:
        delivered_time = data[user_notification.user.id]
        await UsersNotificationsCRUD.update(
            user_notification,
            delivered_time=delivered_time,
            delivered=True,
        )
