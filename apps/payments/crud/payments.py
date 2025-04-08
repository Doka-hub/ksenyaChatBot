from apps.payments.models import RBDetails, Payment
from apps.utils.db import CRUDBase


class RBDetailsCRUD(CRUDBase):
    model = RBDetails
    fields = [
        'id',

        'text',
    ]
    read_only_fields = fields

    @classmethod
    async def create(cls, *args, **kwargs) -> None:
        return None

    @classmethod
    async def update(cls, *args, **kwargs) -> None:
        return None


class PaymentCRUD(CRUDBase):
    model = Payment
    fields = [
        'id',

        'user',
        'channel',
        'stripe_id',
        'amount',
        'type',

        'screenshot',

        'paid_at',

        'is_paid',
    ]
    read_only_fields = ['id']
