from apps.channels.models import Channel
from apps.utils.db import CRUDBase


class ChannelCRUD(CRUDBase):
    model = Channel
    fields = [
        'id',
        'url',
        'eur_amount',
        'rub_amount',
    ]
    read_only_fields = fields

    @classmethod
    async def create(cls, *args, **kwargs) -> None:
        return None

    @classmethod
    async def get_or_create_by_field(cls, *args, **kwargs) -> None:
        return None

    @classmethod
    async def update(cls, *args, **kwargs) -> None:
        return None

