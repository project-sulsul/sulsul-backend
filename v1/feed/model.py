from pydantic import BaseModel

import peewee
from playhouse.signals import Model, pre_save
from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime

from src.orm import db
from src.config.var_config import KST, DB_SCHEMA
from v1.user.model import User


class Feed(Model):
    id = peewee.AutoField(primary_key=True)
    user = peewee.ForeignKeyField(User, backref="user")
    content = BinaryJSONField(default={})
    view_count = peewee.IntegerField(default=0)
    
    class Meta:
        table_name = "feed"
        database = db
        schema = DB_SCHEMA


@pre_save(sender=Feed)
def pre_save(model_class, instance: User, created):
    if not created:
        instance.updated_at = datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")
