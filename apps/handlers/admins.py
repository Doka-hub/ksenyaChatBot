from typing import Any

from aiogram.handlers import MessageHandlerCommandMixin

from apps.utils.handlers import MessageHandler


class DownloadExcelHandler(MessageHandlerCommandMixin, MessageHandler):
    """
    Запуск бота
    """

    async def handle(self) -> Any:
        await self.event.answer_document()
