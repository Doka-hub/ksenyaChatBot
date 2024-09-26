import functools
from abc import ABCMeta
from typing import Any, List, Iterable

from peewee import Model, DoesNotExist
from peewee_async import Manager

from main.db import objects
from .errors import CRUDValidationError


class check_fields:
    def __init__(self, except_fields: List[str] | None = None):
        self._except_fields = except_fields or []

    def __call__(self, func=None):
        if func is None:
            return functools.partial(self.__call__)

        @functools.wraps(func)
        def wrapper(cls, *args, **fields):
            for field in fields.keys():
                if field not in [*cls.fields, *self._except_fields]:
                    raise CRUDValidationError(
                        f'Поле "{field}" не зарегестрировано в "{cls.__name__}.fields". '
                        f'Зарегистрированные поля: "{cls.fields}"'
                    )
            return func(cls, *args, **fields)

        return wrapper


class CRUDBase(metaclass=ABCMeta):
    model: Model

    fields: List[str] = []
    read_only_fields: List[str] = []
    exclude_not_active: bool = True

    # UTILS
    @classmethod
    def get_query_fields(cls) -> List[str]:
        return [getattr(cls.model, field) for field in cls.fields]

    @classmethod
    def get_model_field_condition(cls, field, value):
        return getattr(cls.model, field) == value

    @classmethod
    async def get_first(cls) -> 'model':
        query = await cls.model.select().order_by(cls.model.id).limit(1).aio_execute()
        return query[0]

    # BASE CRUD
    @classmethod
    async def list(cls, *query_filters) -> List[Model]:
        is_active = hasattr(cls.model, 'is_active')
        fields = cls.get_query_fields()
        if is_active and cls.exclude_not_active:
            filter_query = cls.model.select(*fields).filter(cls.model.is_active == True)
        else:
            filter_query = cls.model.select(*fields)

        filter_query = filter_query.filter(*query_filters)

        return await filter_query.aio_execute()

    @classmethod
    @check_fields()
    async def get(cls, **fields) -> Model:
        filter_fields = ((cls.get_model_field_condition(field, fields[field]),) for field in fields)
        query = cls.model.select(*cls.get_query_fields()).where(*filter_fields)
        return await query.aio_get()

    @classmethod
    @check_fields()
    async def create(cls, **fields) -> Model:
        return await cls.model.aio_create(**fields)

    @classmethod
    @check_fields(except_fields=['value'])
    async def get_or_create(cls, **fields) -> tuple[Model, bool]:
        return await cls.model.aio_get_or_create(**fields)

    @classmethod
    @check_fields()
    async def update(cls, instance: Model | Iterable[Model] | int, **fields):
        if not isinstance(instance, Iterable):
            instance_list = [instance]
        else:
            instance_list = instance

        for instance in instance_list:
            data = {}
            if isinstance(instance, int):
                instance = cls.model.aio_get(cls.model.id == instance)

            for field, value in fields.items():
                data[field] = value

            await instance.update(data).aio_execute()

    # SPECIFIC CRUD
    @classmethod
    async def get_by_id(cls, id: int, raise_exception: bool = True) -> Model | None:
        try:
            instance = await cls.get(id=id)
        except DoesNotExist:
            if raise_exception:
                raise DoesNotExist
            instance = None
        return instance

    @classmethod
    async def get_by_field(
        cls,
        field: str,
        value: Any,
        raise_exception: bool = True,
    ) -> Model | None:
        try:
            instance = await cls.get(**{field: value})
        except DoesNotExist:
            if raise_exception:
                raise DoesNotExist
            instance = None
        return instance

    @classmethod
    async def get_or_create_by_field(
        cls,
        field: str,
        value: Any,
    ) -> tuple[Model, bool]:
        instance, created = await cls.get_or_create(**{field: value})
        return instance, created
