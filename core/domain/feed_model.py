from peewee import *
from playhouse.postgres_ext import ArrayField

from core.domain.base_entity import BaseEntity
from core.domain.user_model import User


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

    class Meta:
        table_name = "feed"
