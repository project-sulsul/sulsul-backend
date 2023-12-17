import os, inspect, importlib
from peewee import Model
from playhouse import signals

from core.config.orm_config import db

models = list()
for filename in os.listdir("core/domain"):
    if "_model.py" not in filename:
        continue

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

feed_data = [
    {
        "user_id": 1,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "tags": "삼겹살,소주",
        "images": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg,https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
    },
    {
        "user_id": 1,
        "title": "회쏘굳1",
        "content": "회는 굳잡맨 맛나요 짱짱 굳1",
        "tags": "회,소주",
        "images": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg,https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg",
    },
    {
        "user_id": 2,
        "title": "회쏘굳2",
        "content": "회는 굳잡맨 맛나요 짱짱 굳2",
        "tags": "회,소주",
        "images": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg,https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg",
    },
]
for record in feed_data:
    Feed.create(**record)

from core.domain.feed_like_model import FeedLike

feed_like_data = [
    {"user_id": 1, "feed_id": 1},
    {"user_id": 1, "feed_id": 2},
    {"user_id": 2, "feed_id": 1},
    {"user_id": 2, "feed_id": 2},
]
for record in feed_like_data:
    FeedLike.create(**record)

from core.domain.pairing_model import Pairing

pairing_data = [
    {
        "type": "술",
        "subtype": "소주",
        "name": ["처음처럼", "참이슬", "좋은데이", "진로", "새로"],
        "image": None,
    },
    {
        "type": "술",
        "subtype": "맥주",
        "name": ["카스", "클라우드", "테라", "하이트", "오비"],
        "image": None,
    },
    {"type": "술", "subtype": "하이볼", "name": ["하이볼"], "image": None},
    {"type": "술", "subtype": "막걸리", "name": ["막걸리"], "image": None},
    {"type": "술", "subtype": "와인", "name": ["와인"], "image": None},
    {"type": "안주", "subtype": "패스트푸드", "name": ["피자"], "image": None},
    {
        "type": "안주",
        "subtype": "육류",
        "name": ["삼겹살", "소고기", "족발", "육회", "곱창", "양꼬치", "닭갈비", "닭발"],
        "image": None,
    },
    {"type": "안주", "subtype": "탕류", "name": ["어묵탕", "짬뽕탕", "나가사키 짬뽕"], "image": None},
    {"type": "안주", "subtype": "튀김류", "name": ["치킨", "감자튀김", "새우튀김"], "image": None},
    {"type": "안주", "subtype": "과일", "name": ["화채", "파인애플", "황도"], "image": None},
    {"type": "안주", "subtype": "과자", "name": ["나쵸"], "image": None},
    {"type": "안주", "subtype": "밥류", "name": ["두부김치", "계란말이", "국밥"], "image": None},
    {"type": "안주", "subtype": "면류", "name": ["짜파게티"], "image": None},
    {"type": "안주", "subtype": "회", "name": ["연어", "광어/우럭"], "image": None},
    {"type": "안주", "subtype": "마른안주", "name": ["먹태", "육포", "오징어"], "image": None},
]
real_pairing_data = []
for pairing in pairing_data:
    for name in pairing["name"]:
        real_pairing_data.append(
            {
                "type": pairing["type"],
                "subtype": pairing["subtype"],
                "name": name,
                "image": pairing["image"],
                "description": f"{name}입니다",
            }
        )

for record in real_pairing_data:
    Pairing.create(**record)

db.close()
