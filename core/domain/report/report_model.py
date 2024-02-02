from enum import Enum

import peewee

from core.domain.base_entity import BaseEntity
from core.domain.user.user_model import User


class Report(BaseEntity):
    reporter = peewee.ForeignKeyField(User, backref="user")
    type = peewee.CharField(max_length=500, null=False)  # feed, comment
    target_id = peewee.IntegerField(null=False)
    reason = peewee.CharField(max_length=500, null=False)
    status = peewee.CharField(max_length=500, null=False)  # ReportStatus

    class Meta:
        table_name = "report"


class ReportStatus(Enum):
    PENDING = "PENDING"
    SOLVED = "SOLVED"
