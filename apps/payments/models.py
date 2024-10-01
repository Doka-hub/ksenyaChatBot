from datetime import datetime
from enum import Enum

import peewee

from apps.channels.models import Channel
from apps.users.models import TGUser
from apps.utils.models import BaseModel


class PaymentType(Enum):
    EU = 'eur'
    RB = 'rub'


class RBDetails(BaseModel):
    account_number = peewee.CharField(max_length=255)
    field_1 = peewee.CharField(max_length=255)
    field_2 = peewee.CharField(max_length=255)


class Payment(BaseModel):
    user = peewee.ForeignKeyField(TGUser, backref='payments', on_delete='CASCADE')
    stripe_id = peewee.CharField(max_length=255, null=True, verbose_name='Stripe ID')
    amount = peewee.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    type = peewee.CharField(
        max_length=20,
        choices=PaymentType,
        verbose_name='Тип Оплаты',
    )
    screenshot = peewee.CharField(max_length=255, verbose_name='Путь к фалу', null=True)
    created_at = peewee.DateTimeField(default=datetime.now)
    paid_at = peewee.DateTimeField(null=True)

    is_paid = peewee.BooleanField(default=False, verbose_name='Оплачено')


class Subscription(BaseModel):
    payment = peewee.ForeignKeyField(
        Payment,
        unique=True,
        backref='subscription',
        on_delete='CASCADE'
    )
    user = peewee.ForeignKeyField(TGUser, backref='subscriptions', on_delete='CASCADE')
    channel = peewee.ForeignKeyField(
        Channel,
        backref='subscriptions',
        on_delete='SET NULL',
        null=True,
    )

    created_at = peewee.DateTimeField(default=datetime.now)
    active_by = peewee.DateTimeField(null=True)
