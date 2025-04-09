from enum import Enum
from typing import TypeVar

from pydantic import BaseModel


T = TypeVar('T', bound=Enum)
ImageURL = TypeVar('ImageURL', bound=str)
ImageBytes = TypeVar('ImageBytes', bound=bytes)

FileURL = TypeVar('FileURL', bound=str)
FileBytes = TypeVar('FileBytes', bound=bytes)

TGUserID = TypeVar('TGUserID', bound=str | int)
UserID = TypeVar('UserID', bound=str | int)


class TypeBaseEnum(Enum):
    @classmethod
    def get_type(cls, name: str | T | None = None):
        if isinstance(name, cls):
            type_ = name
        else:
            type_ = cls(name)
        return type_


class NotificationType(TypeBaseEnum):
    DEFAULT = 'default'
    PAYMENT_TO_REVIEW = 'payment_to_review'


class BaseNotifyUsers(BaseModel):
    type: NotificationType
    message: str | None

    class Config:
        use_enum_values = True


class NotifyUsers(BaseNotifyUsers):
    users_ids: list[tuple[UserID, TGUserID]] | None
    notification_id: int | None


class PaymentNotifyUser(BaseNotifyUsers):
    order_id: int
    file: FileURL | FileBytes | None
