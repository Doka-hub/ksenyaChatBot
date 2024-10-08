from enum import Enum


class ResponseType(Enum):
    text = 'text'
    number = 'number'
    email = 'email'
    media = 'media'
    date = 'date'


class ResponseStatus(Enum):
    waiting = 'waiting'
    received = 'received'
    timeout = 'timeout'
