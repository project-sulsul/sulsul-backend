from enum import Enum

import peewee

from core.domain.base_entity import BaseEntity


class Pairing(BaseEntity):
    type = peewee.CharField(max_length=10, null=False)
    subtype = peewee.CharField(max_length=100, null=True)
    name = peewee.CharField(max_length=100, null=False, unique=True)
    image = peewee.CharField(null=True, default=None)
    description = peewee.CharField(null=True)

    class Meta:
        table_name = "pairing"
