from datetime import datetime

import peewee

from apps.users.models import TGUser
from apps.utils.fields import FileField
from apps.utils.models import BaseModel


class Notification(BaseModel):
    users = peewee.ManyToManyField(
        TGUser,
        backref='notifications',
    )
    text = peewee.TextField()

    send_separately = peewee.BooleanField(default=False)
    filters = peewee.CharField(max_length=255)
    send_all = peewee.BooleanField(default=False)

    created = peewee.DateTimeField(default=datetime.now)


class NotificationButton(BaseModel):
    notification = peewee.ForeignKeyField(
        Notification,
        on_delete='CASCADE',
        related_name='buttons',
        verbose_name='Уведомление',
    )
    text = peewee.CharField(max_length=255, verbose_name='Текст')
    url = peewee.CharField(null=True, verbose_name='Ссылка')


class NotificationImage(BaseModel):
    notification = peewee.ForeignKeyField(
        Notification,
        on_delete='CASCADE',
        related_name='images',
        verbose_name='Уведомление',
    )
    image = FileField()


class UsersNotifications(BaseModel):
    user = peewee.ForeignKeyField(TGUser, index=True, backref='notifications')
    notification = peewee.ForeignKeyField(Notification, backref='users', index=True)
    delivered = peewee.BooleanField(default=False)
    delivered_time = peewee.DateTimeField(null=True)
