import peewee

from core.domain.base_entity import BaseEntity
from core.domain.pairing.pairing_model import Pairing


class Combination(BaseEntity):
    alcohol = peewee.ForeignKeyField(Pairing)
    food = peewee.ForeignKeyField(Pairing)
    description = peewee.CharField(max_length=1000, null=True, default=None)
    count = peewee.BigIntegerField(default=0)

    class Meta:
        table_name = "combination"
