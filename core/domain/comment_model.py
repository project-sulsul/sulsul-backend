import peewee

from core.domain.base_entity import BaseEntity
from core.domain.feed_model import Feed
from core.domain.user_model import User


class Comment(BaseEntity):
    user = peewee.ForeignKeyField(User, backref="user")
    feed = peewee.ForeignKeyField(Feed, backref="feed")
    content = peewee.CharField(max_length=1000, null=False)
    parent_comment = peewee.ForeignKeyField(
        "self", backref="children_comments", null=True
    )
    is_reported = peewee.BooleanField(default=False)

    class Meta:
        table_name = "comment"
