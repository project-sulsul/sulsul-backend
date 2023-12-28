from peewee import *
from playhouse.postgres_ext import ArrayField

from api.config.exceptions import ForbiddenException
from core.domain.base_entity import BaseEntity
from core.domain.user.user_model import User


class Feed(BaseEntity):
    user = ForeignKeyField(User, backref="user")
    title = CharField(max_length=100, null=False)
    content = CharField(max_length=500, null=False)
    score = DoubleField(default=0.0)
    represent_image = CharField(null=False)
    images = ArrayField(CharField, null=False)
    classify_tags = ArrayField(
        CharField, null=False
    )  # 모델이 추론한 or 유저가 보정한 사진에 대한 술,안주 분류 태그
    user_tags = ArrayField(CharField, null=True)
    view_count = IntegerField(default=0)

    def check_if_owner(self, user_id: int):
        if self.user.id != user_id:
            raise ForbiddenException(f"feed(id:{self.id}) is not yours")

    class Meta:
        table_name = "feed"
