import peewee
from playhouse.signals import Model, pre_save
from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime

from core.config.orm_config import db
from core.config.var_config import KST, DB_SCHEMA


class User(Model):
    id = peewee.AutoField(primary_key=True)
    uid = peewee.CharField(max_length=100, null=False, unique=True)
    social_type = peewee.CharField(max_length=10, null=True)
    nickname = peewee.CharField(max_length=30, null=True)
    preference = BinaryJSONField(default={})
    status = peewee.CharField(max_length=10, default="active")
    created_at = peewee.DateTimeField(
        default=datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")
    )
    updated_at = peewee.DateTimeField(
        default=datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")
    )
    is_deleted = peewee.BooleanField(default=False)

    class Meta:
        table_name = "user"
        database = db
        schema = DB_SCHEMA

    def __getitem__(self, key: str):
        return self.__data__[key]

    def __setitem__(self, key, value):
        self.__data__[key] = value


@pre_save(sender=User)
def pre_save(model_class, instance: User, created):
    if not created:
        instance.updated_at = datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")
