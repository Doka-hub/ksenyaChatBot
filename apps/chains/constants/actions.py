from enum import Enum


class ActionName(Enum):
    ban = 'ban'
    unban = 'unban'

    add_tag = 'tag'
    delete_tag = 'delete_tag'

    set_attr = 'set_attr'
    del_attr = 'del_attr'
