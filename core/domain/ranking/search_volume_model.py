from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField

from core.config.var_config import KST
from core.domain.base_entity import BaseEntity


class SearchVolume(BaseEntity):
    name = CharField(max_length=100, null=False)
    volume = IntegerField(default=0, null=False)
    start_date = DateTimeField(default=datetime.now(KST).strftime("%Y-%m-%d"))
    end_date = DateTimeField(default=datetime.now(KST).strftime("%Y-%m-%d"))

    class Meta:
        table_name = "search_volume"
