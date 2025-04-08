# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class StartMessage(peewee.Model):
    type = CharField(max_length=255)
    text = TextField()
    photo = CharField(max_length=255, null=True)
    video = CharField(max_length=255, null=True)
    class Meta:
        table_name = "startmessage"


@snapshot.append
class ButtonMessage(peewee.Model):
    message = snapshot.ForeignKeyField(backref='buttons', index=True, model='startmessage')
    type = CharField(max_length=10)
    name = CharField(max_length=255)
    url = CharField(max_length=255, null=True)
    callback_data = CharField(max_length=255, null=True)
    class Meta:
        table_name = "buttonmessage"


@snapshot.append
class Channel(peewee.Model):
    name = CharField(max_length=255)
    url = CharField(max_length=255)
    eur_amount = DecimalField(auto_round=False, decimal_places=2, max_digits=10, rounding='ROUND_HALF_EVEN')
    rub_amount = DecimalField(auto_round=False, decimal_places=2, max_digits=10, rounding='ROUND_HALF_EVEN')
    duration = IntegerField(default=30)
    class Meta:
        table_name = "channel"


@snapshot.append
class Notification(peewee.Model):
    text = TextField()
    send_separately = BooleanField(default=False)
    send_all = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "notification"


@snapshot.append
class TGUser(peewee.Model):
    user_id = CharField(max_length=255)
    username = CharField(max_length=255, null=True)
    role = CharField(default='CLIENT', max_length=255)
    first_name = CharField(max_length=255, null=True)
    last_name = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    phone_number = CharField(max_length=255, null=True)
    is_bot_blocked = BooleanField(default=False)
    is_active = BooleanField(default=True)
    policy_confirmed = BooleanField(default=False)
    class Meta:
        table_name = "tguser"


@snapshot.append
class Payment(peewee.Model):
    user = snapshot.ForeignKeyField(backref='payments', index=True, model='tguser', on_delete='CASCADE')
    channel = snapshot.ForeignKeyField(backref='payments', index=True, model='channel', null=True, on_delete='SET NULL')
    stripe_id = CharField(max_length=255, null=True)
    amount = DecimalField(auto_round=False, decimal_places=2, max_digits=10, rounding='ROUND_HALF_EVEN')
    type = CharField(max_length=20)
    screenshot = CharField(max_length=255, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    paid_at = DateTimeField(null=True)
    is_paid = BooleanField(default=False)
    class Meta:
        table_name = "payment"


@snapshot.append
class RBDetails(peewee.Model):
    text = TextField(default='text')
    class Meta:
        table_name = "rbdetails"


@snapshot.append
class Subscription(peewee.Model):
    payment = snapshot.ForeignKeyField(backref='subscription', index=True, model='payment', on_delete='CASCADE', unique=True)
    user = snapshot.ForeignKeyField(backref='subscriptions', index=True, model='tguser', on_delete='CASCADE')
    channel = snapshot.ForeignKeyField(backref='subscriptions', index=True, model='channel', null=True, on_delete='SET NULL')
    created_at = DateTimeField(default=datetime.datetime.now)
    active_by = DateTimeField(null=True)
    class Meta:
        table_name = "subscription"


@snapshot.append
class UsersNotifications(peewee.Model):
    user = snapshot.ForeignKeyField(backref='notifications', index=True, model='tguser')
    notification = snapshot.ForeignKeyField(backref='users', index=True, model='notification')
    delivered = BooleanField(default=False)
    delivered_time = DateTimeField(null=True)
    class Meta:
        table_name = "usersnotifications"


def forward(old_orm, new_orm):
    startmessage = new_orm['startmessage']
    return [
        # Apply default value '' to the field startmessage.type,
        startmessage.update({startmessage.type: ''}).where(startmessage.type.is_null(True)),
    ]


def migrate_forward(op, old_orm, new_orm):
    op.add_column(new_orm.startmessage.type)
    op.run_data_migration()
    op.add_not_null(new_orm.startmessage.type)


def migrate_backward(op, old_orm, new_orm):
    op.run_data_migration()
    op.drop_column(old_orm.startmessage.type)
