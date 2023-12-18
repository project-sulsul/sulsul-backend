import peewee

from core.domain.base_entity import BaseEntity
from core.domain.user_model import User


class Feed(BaseEntity):
    user = peewee.ForeignKeyField(User, backref="user")
    title = peewee.CharField(max_length=100, null=False)
    content = peewee.CharField(max_length=500, null=False)
    score = peewee.DoubleField(default=0.0)
    images = peewee.CharField(null=True)  # separate by comma
    tags = peewee.CharField(null=True)  # separate by comma
    view_count = peewee.IntegerField(default=0)

    class Meta:
        table_name = "feed"
