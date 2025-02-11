from aiogram import Bot

from aiogram.types import BotCommand

StartCommand = BotCommand(command='start', description='Запустить бота')
DownloadExcelCommand = BotCommand(command='excel', description='Скачать excel')


async def set_bot_commands(bot: Bot):
    commands = [
        StartCommand
    ]
    await bot.set_my_commands(commands=commands)


async def set_manager_bot_commands(bot: Bot):
    commands = [
        StartCommand,
        DownloadExcelCommand,
    ]
    bot.set_my_commands()
    await bot.set_my_commands(commands=commands)
