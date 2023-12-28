import peewee

from core.domain.base_entity import BaseEntity
from core.domain.feed.feed_model import Feed
from core.domain.user.user_model import User


class FeedLike(BaseEntity):
    user = peewee.ForeignKeyField(User, backref="user")
    feed = peewee.ForeignKeyField(Feed, backref="feed")

    class Meta:
        table_name = "feed_like"
