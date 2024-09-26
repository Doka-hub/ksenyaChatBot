import re
from datetime import datetime, timedelta

from apps.payments.models import Payment
from .models import TGUser


async def get_user_payments(user: TGUser):
    paid_date = datetime.now() - timedelta(days=30)
    user_payments = await Payment.filter(
        Payment.is_paid == True,
        Payment.paid_at >= paid_date,
        Payment.user == user,
    ).aio_execute()
    return user_payments


async def is_user_paid(user: TGUser):
    return len(await get_user_payments(user)) >= 1


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
