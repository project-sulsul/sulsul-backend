import peewee

from api.config.exceptions import ForbiddenException
from core.domain.base_entity import BaseEntity
from core.domain.feed.feed_model import Feed
from core.domain.user.user_model import User


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

    def update_content(self, content):
        self.content = content
        self.save()

    def check_if_owner(self, user_id: int):
        if self.user.id != user_id:
            raise ForbiddenException(f"comment(id:{self.id}) is not yours")
