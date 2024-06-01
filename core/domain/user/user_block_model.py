import peewee

from core.domain.base_entity import BaseEntity
from core.domain.user.user_model import User


class UserBlock(BaseEntity):
    user = peewee.ForeignKeyField(User, backref="user")
    blocked_user = peewee.ForeignKeyField(User, backref="blocked_user")

    class Meta:
        table_name = "user_block"
