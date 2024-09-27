from typing import Any
from io import BytesIO
import pandas as pd

from aiogram.handlers import MessageHandlerCommandMixin
from aiogram.types import BufferedInputFile

from apps.utils.handlers import MessageHandler
from apps.users.crud import TGUserCRUD
from apps.users.models import TGUser


class DownloadExcelHandler(MessageHandlerCommandMixin, MessageHandler):
    """
    Запуск бота
    """

    async def handle(self) -> Any:
        users_data = {
            'username': [],
            'email': [],
        }
        users: list[TGUser] = await TGUserCRUD.list()
        for user in users:
            users_data['username'].append(user.username)
            users_data['email'].append(user.email)
        # excel_file_path = f'media/excels/{request.user.id}'
        # if not os.path.exists(excel_file_path):
        #     os.makedirs(excel_file_path, exist_ok=True)
        # excel_file_name = excel_file_path + f'{uuid4()}.xlsx'
        bytesio = BytesIO()
        df = pd.DataFrame(users_data)
        with pd.ExcelWriter(bytesio, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        bytesio.seek(0)
        await self.event.answer(
            'Отправляю файл'
        )
        await self.event.answer_document(BufferedInputFile(bytesio, 'excel.xlsx'))
