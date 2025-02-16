from enum import Enum

import peewee

from apps.utils.models import BaseModel


class Role(Enum):
    client = 'CLIENT'
    manager = 'MANAGER'


class TGUser(BaseModel):
    user_id = peewee.CharField(max_length=255)
    username = peewee.CharField(max_length=255, null=True)
    role = peewee.CharField(max_length=255, choices=Role, default='CLIENT')

    first_name = peewee.CharField(max_length=255, null=True)
    last_name = peewee.CharField(max_length=255, null=True)

    email = peewee.CharField(max_length=255, null=True)
    phone_number = peewee.CharField(max_length=255, null=True)

    is_bot_blocked = peewee.BooleanField(default=False)
    is_active = peewee.BooleanField(default=True)
    policy_confirmed = peewee.BooleanField(default=False)

    @property
    def is_manager(self):
        return Role(self.role) == Role.manager


class ButtonMessage(BaseModel):
    class Type(Enum):
        INLINE = 'INLINE', 'Inline'
        KEYBOARD = 'KEYBOARD', 'Keyboard'

    type = peewee.CharField(verbose_name='Тип', max_length=10)
    name = peewee.CharField(max_length=255, verbose_name='Название')
    url = peewee.CharField(null=True, verbose_name='Ссылка')
    callback_data = peewee.CharField(
        max_length=255,
        null=True,
        verbose_name='Callback Data',
    )

    def __str__(self):
        return f'{self.type} кнопка: {self.name}'


class StartMessage(BaseModel):
    text = peewee.TextField()
    photo = peewee.CharField(max_length=255, null=True, verbose_name='Ссылка на фото')
    video = peewee.CharField(max_length=255, null=True, verbose_name='Ссылка на видео')
    buttons = peewee.ManyToManyField(ButtonMessage, backref='messages', on_delete='SET NULL')
