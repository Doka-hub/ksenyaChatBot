import peewee

from apps.utils.models import BaseModel


class Channel(BaseModel):
    name = peewee.CharField()
    telegram_chat_id = peewee.CharField()
    url = peewee.CharField(max_length=255)
    eur_amount = peewee.DecimalField(max_digits=10, decimal_places=2)
    rub_amount = peewee.DecimalField(max_digits=10, decimal_places=2)
    duration = peewee.IntegerField(default=30)
