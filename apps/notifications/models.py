from datetime import datetime

import peewee

from apps.users.models import TGUser
from apps.utils.models import BaseModel


class Notification(BaseModel):
    users = peewee.ManyToManyField(
        TGUser,
        backref='notifications',
    )
    text = peewee.TextField()

    send_separately = peewee.BooleanField(default=False)
    send_all = peewee.BooleanField(default=False)

    created = peewee.DateTimeField(default=datetime.now)


class UsersNotifications(BaseModel):
    user = peewee.ForeignKeyField(TGUser, index=True, backref='notifications')
    notification = peewee.ForeignKeyField(Notification, backref='users', index=True)
    delivered = peewee.BooleanField(default=False)
    delivered_time = peewee.DateTimeField(null=True)
