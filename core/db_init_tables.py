import os, inspect, importlib
from peewee import Model
from playhouse import signals

from core.config.orm_config import db


models = list()
for filename in os.listdir("core/domain"):
    if "_model.py" not in filename: continue

    model_module = "core.domain." + filename.split(".")[0]
    model = importlib.import_module(model_module)
    models.extend(
        [
            obj
            for _, obj in inspect.getmembers(model)
            if inspect.isclass(obj)
            and issubclass(obj, Model)
            and obj is not Model
            and obj is not signals.Model
        ]
    )

db.connect()

from admin.model import Admin

db.create_tables([Admin], safe=True)

db.drop_tables(models)
db.create_tables(models)

from core.domain.user_model import User

user_data = [
    {"uid": "ahdwjdtprtm@gmail.com", "social_type": "google", "nickname": "user1"},
    {"uid": "iee785@daum.net", "social_type": "kakao", "nickname": "user2"},
    {"uid": "tmlee@pluszero.co.kr", "social_type": "google", "nickname": "user3"},
]
for record in user_data:
    User.create(**record)

from core.domain.feed_model import Feed

feed_data = [{"user_id": 1}, {"user_id": 1}, {"user_id": 1}, {"user_id": 2}]
for record in feed_data:
    Feed.create(**record)

from core.domain.pairing_model import Pairing

pairing_data = [
    {"type": "술", "name": "소주", "image": None, "description": "소주예요"},
    {"type": "술", "name": "맥주", "image": None, "description": "맥주예요"},
    {"type": "술", "name": "하이볼", "image": None, "description": "하이볼이에요"},
    {"type": "술", "name": "막걸리", "image": None, "description": "막걸리예요"},
    {"type": "술", "name": "와인", "image": None, "description": "와인이에요"},
    {"type": "안주", "name": "패스트푸드", "image": None, "description": "패스트푸드예요"},
    {"type": "안주", "name": "육류", "image": None, "description": "육류예요"},
    {"type": "안주", "name": "탕류", "image": None, "description": "탕류예요"},
    {"type": "안주", "name": "튀김류", "image": None, "description": "튀김류예요"},
    {"type": "안주", "name": "과일", "image": None, "description": "과일이에요"},
    {"type": "안주", "name": "과자", "image": None, "description": "과자예요"},
    {"type": "안주", "name": "면류", "image": None, "description": "면류예요"},
    {"type": "안주", "name": "회", "image": None, "description": "회예요"},
    {"type": "안주", "name": "마른안주", "image": None, "description": "마른안주예요"},
]
for record in pairing_data:
    Pairing.create(**record)

db.close()
