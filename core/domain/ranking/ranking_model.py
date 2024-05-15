import peewee
from playhouse.postgres_ext import BinaryJSONField

from core.domain.base_entity import BaseEntity


class Ranking(BaseEntity):
    start_date = peewee.DateTimeField()
    end_date = peewee.DateTimeField()
    ranking = BinaryJSONField(default={})

    class Meta:
        table_name = "ranking"