from datetime import datetime

import peewee

from apps.utils.models import BaseModel
from .constants.actions import ActionName
from .constants.attributes import Attribute, Compare
from .constants.button_types import ButtonType
from .constants.user_responses import ResponseType, ResponseStatus


class Trigger(BaseModel):
    name = peewee.CharField(max_length=255)


class Chain(BaseModel):
    trigger = peewee.ForeignKeyField(
        Trigger,
        backref='chain',
        on_delete='SET NULL',
        unique=True,
        null=True,
    )
    name = peewee.CharField(max_length=255)


class Stage(BaseModel):
    chain = peewee.ForeignKeyField(
        Chain,
        backref='messages',
        on_delete='CASCADE',
    )
    order = peewee.IntegerField()


class Message(BaseModel):
    stage = peewee.ForeignKeyField(Stage, backref='messages', on_delete='CASCADE')
    text = peewee.CharField(max_length=255)

    next_stage = peewee.ForeignKeyField(
        Stage,
        backref='from_messages',
        on_delete='SET NULL',
        null=True,
    )

    wait_response = peewee.BooleanField(default=False)


class MessageButton(BaseModel):
    message = peewee.ForeignKeyField(Message, backref='buttons', on_delete='CASCADE')
    text = peewee.CharField(max_length=255)
    type = peewee.CharField(max_length=20, choices=ButtonType)

    next_stage = peewee.ForeignKeyField(
        Stage,
        backref='from_buttons',
        on_delete='SET NULL',
        unique=True,
        null=True,
    )


class UserResponse(BaseModel):
    class Meta:
        indexes = (
            (('user_id', 'stage'), True),  # Создание уникального составного индекса
        )

    stage = peewee.ForeignKeyField(Stage, backref='user_responses', on_delete='CASCADE')
    user_id = peewee.CharField(max_length=255)

    value_type = peewee.CharField(max_length=255, choices=ResponseType)
    status = peewee.CharField(max_length=255, choices=ResponseStatus)

    started_at = peewee.DateTimeField(default=datetime.now)
    timeout_seconds = peewee.IntegerField(default=300)


class Action(BaseModel):
    stage = peewee.ForeignKeyField(Stage, backref='actions', on_delete='CASCADE')
    name = peewee.CharField(max_length=255, choices=ActionName)


class Condition(BaseModel):
    stage = peewee.ForeignKeyField(Stage, backref='conditions', on_delete='CASCADE')

    attr = peewee.CharField(max_length=255, choices=Attribute)
    compare = peewee.CharField(max_length=255, choices=Compare, null=True)
    value = peewee.CharField(max_length=255)

    next_stage = peewee.ForeignKeyField(
        Stage,
        backref='from_conditions',
        on_delete='SET NULL',
        unique=True,
        null=True,
    )


class UserProgress(BaseModel):
    user_id = peewee.BigIntegerField()
    chain = peewee.ForeignKeyField(Chain, backref='user_progresses', on_delete='CASCADE')
    current_stage = peewee.ForeignKeyField(
        Stage,
        on_delete='SET NULL',
        null=True
    )
    started_at = peewee.DateTimeField(auto_now_add=True)
    updated_at = peewee.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Прогресс пользователя {self.user_id} в цепочке {self.chain.name}"
