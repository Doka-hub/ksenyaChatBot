# auto-generated snapshot
from peewee import *
import apps.utils.fields
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Channel(peewee.Model):
    name = CharField(max_length=255)
    url = CharField(max_length=255)
    eur_amount = DecimalField(auto_round=False, decimal_places=2, max_digits=10, rounding='ROUND_HALF_EVEN')
    rub_amount = DecimalField(auto_round=False, decimal_places=2, max_digits=10, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "channel"


@snapshot.append
class Notification(peewee.Model):
    text = TextField()
    image = apps.utils.fields.FileField(max_length=100, null=True)
    file = apps.utils.fields.FileField(max_length=100, null=True)
    send_separately = BooleanField(default=False)
    send_all = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "notification"


@snapshot.append
class TGUser(peewee.Model):
    user_id = CharField(max_length=255)
    username = CharField(max_length=255, null=True)
    role = CharField(default='client', max_length=255)
    first_name = CharField(max_length=255, null=True)
    last_name = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    phone_number = CharField(max_length=255, null=True)
    is_bot_blocked = BooleanField(default=False)
    is_active = BooleanField(default=True)
    class Meta:
        table_name = "tguser"


@snapshot.append
class Payment(peewee.Model):
    user = snapshot.ForeignKeyField(backref='payments', index=True, model='tguser', on_delete='CASCADE')
    stripe_id = CharField(max_length=255, null=True)
    amount = DecimalField(auto_round=False, decimal_places=2, max_digits=10, rounding='ROUND_HALF_EVEN')
    type = CharField(max_length=20)
    created_at = DateTimeField(default=datetime.datetime.now)
    is_paid = BooleanField(default=False)
    class Meta:
        table_name = "payment"


@snapshot.append
class RBDetails(peewee.Model):
    account_number = CharField(max_length=255)
    field_1 = CharField(max_length=255)
    field_2 = CharField(max_length=255)
    class Meta:
        table_name = "rbdetails"


@snapshot.append
class UsersNotifications(peewee.Model):
    user = snapshot.ForeignKeyField(backref='notifications', index=True, model='tguser')
    notification = snapshot.ForeignKeyField(backref='users', index=True, model='notification')
    delivered = BooleanField(default=False)
    delivered_time = DateTimeField(null=True)
    class Meta:
        table_name = "usersnotifications"


def migrate_forward(op, old_orm, new_orm):
    op.create_table(new_orm.channel)
    op.create_table(new_orm.notification)
    op.create_table(new_orm.tguser)
    op.create_table(new_orm.payment)
    op.create_table(new_orm.rbdetails)
    op.create_table(new_orm.usersnotifications)
    op.run_data_migration()


def migrate_backward(op, old_orm, new_orm):
    op.run_data_migration()
    op.drop_table(old_orm.usersnotifications)
    op.drop_table(old_orm.rbdetails)
    op.drop_table(old_orm.payment)
    op.drop_table(old_orm.tguser)
    op.drop_table(old_orm.notification)
    op.drop_table(old_orm.channel)
