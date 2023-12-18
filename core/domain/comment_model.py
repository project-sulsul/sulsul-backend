import peewee

from core.domain.base_entity import BaseEntity
from core.domain.feed_model import Feed
from core.domain.user_model import User


class Comment(BaseEntity):
    writer = peewee.ForeignKeyField(User, backref="user")
    feed = peewee.ForeignKeyField(Feed, backref="feed")
    is_reported = peewee.BooleanField(default=False)

    class Meta:
        table_name = "comment"
