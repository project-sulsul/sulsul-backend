import peewee
from playhouse.signals import Model, pre_save
from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime

from core.config.orm_config import db
from core.config.var_config import KST, DB_SCHEMA
from core.domain.base_entity import BaseEntity
from core.domain.user_model import User


class Feed(BaseEntity):
    user = peewee.ForeignKeyField(User, backref="user")
    content = BinaryJSONField(default={})
    view_count = peewee.IntegerField(default=0)

    class Meta:
        table_name = "feed"
