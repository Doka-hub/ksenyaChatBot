from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Запустить бота'),
    ]
    await bot.set_my_commands(commands=commands)


async def set_manager_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Запустить бота'),
        BotCommand(command='payments', description='Скачать платежи (excel)'),
    ]
    await bot.set_my_commands(commands=commands)

