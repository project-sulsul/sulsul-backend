from datetime import datetime

import peewee
from playhouse.signals import Model, pre_save

from core.config.orm_config import db
from core.config.var_config import KST, DB_SCHEMA
from core.domain.base_entity import BaseEntity


class Pairing(Model):
    id = peewee.AutoField(primary_key=True)
    type = peewee.CharField(max_length=10, null=False)
    subtype = peewee.CharField(max_length=100, null=True)
    name = peewee.CharField(max_length=100, null=False, unique=True)
    image = peewee.CharField(null=True)
    description = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(
        default=datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")
    )
    updated_at = peewee.DateTimeField(
        default=datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")
    )
    is_deleted = peewee.BooleanField(default=False)

    class Meta:
        table_name = "pairing"
        database = db
        schema = DB_SCHEMA


@pre_save(sender=Pairing)
def pre_save(model_class, instance: Pairing, created):
    if not created:
        instance.updated_at = datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z")


class PairingRequest(BaseEntity):
    type = peewee.CharField(max_length=10, null=False)  # 술, 안주
    subtype = peewee.CharField(max_length=100, null=True)  # 육류, 마른안주 등
    name = peewee.CharField(max_length=100, null=False, unique=True)

    class Meta:
        table_name = "pairing_request"
