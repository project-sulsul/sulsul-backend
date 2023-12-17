import peewee

from core.domain.base_entity import BaseEntity
from core.domain.user_model import User


class Report(BaseEntity):
    reporter = peewee.ForeignKeyField(User, backref="user")
    type = peewee.CharField(max_length=500, null=False)  # feed, comment
    target_id = peewee.IntegerField(null=False)
    reason = peewee.CharField(max_length=500, null=False)

    class Meta:
        table_name = "report"
