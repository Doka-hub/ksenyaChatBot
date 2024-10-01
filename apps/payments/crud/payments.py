from apps.payments.models import RBDetails, Payment
from apps.utils.db import CRUDBase


class RBDetailsCRUD(CRUDBase):
    model = RBDetails
    fields = [
        'id',

        'account_number',
        'field_1',
        'field_1',
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
        'stripe_id',
        'amount',
        'type',

        'screenshot',

        'paid_at',
        'active_by',

        'is_paid',
    ]
    read_only_fields = ['id']
