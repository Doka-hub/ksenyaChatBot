from apps.notifications.models import Notification, UsersNotifications
from apps.utils.db import CRUDBase


class NotificationCRUD(CRUDBase):
    model = Notification
    fields = ['id', 'text', 'send', 'delivered', 'delivered_time']
    read_only_fields = ['id']


class UsersNotificationsCRUD(CRUDBase):
    model = UsersNotifications
    fields = ['id', 'user', 'notification', 'delivered', 'delivered_time']
    read_only_fields = ['id']
