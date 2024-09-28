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

    @property
    def is_manager(self):
        return Role(self.role) == Role.manager


class StartMessage(BaseModel):
    text = peewee.TextField()
    photo = peewee.CharField(max_length=255, verbose_name='Ссылка на фото')
    video = peewee.CharField(max_length=255, verbose_name='Ссылка на видео')
