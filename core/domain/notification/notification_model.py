from peewee import ForeignKeyField, CharField

from core.domain.base_entity import BaseEntity
from core.domain.user.user_model import User


class Notification(BaseEntity):
    send_user = ForeignKeyField(User, backref="user")
    receive_user = ForeignKeyField(User, backref="user")

    title = CharField(max_length=100, null=False)
    content = CharField(max_length=500, null=False)

    class Meta:
        table_name = "notification"
