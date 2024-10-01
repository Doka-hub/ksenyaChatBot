from apps.users.models import TGUser
from apps.utils.db import CRUDBase


class TGUserCRUD(CRUDBase):
    model = TGUser
    fields = [
        'id',

        'user_id',
        'username',

        'first_name',
        'last_name',

        'email',
        'phone_number',
    ]
    read_only_fields = ['id']

    @classmethod
    async def bot_block(cls, user: TGUser | int):
        if isinstance(user, int):
            user = await cls.get_by_field('user_id', user)

        await cls.update(user, is_active=False, is_bot_blocked=True)

    @classmethod
    async def bot_unblock(cls, user: TGUser | int):
        if isinstance(user, int):
            user = await cls.get_by_field('user_id', user)

        await cls.update(user, is_active=True, is_bot_blocked=False)
