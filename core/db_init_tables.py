import importlib
import inspect
import os
import random

from peewee import Model
from playhouse import signals

from core.config.orm_config import db
from core.domain.base_entity import BaseEntity


def scan_domain_models():
    models = list()
    model_package_paths = list()
    domain_root = "core/domain"
    for root, dirs, files in os.walk(domain_root):
        for dir_name in dirs:
            dir = f"{domain_root}/{dir_name}"
            for file in os.listdir(dir):
                if file.endswith("_model.py"):
                    model_package_paths.append(f"{dir_name}.{file.split('.')[0]}")

    for package_path in model_package_paths:
        model_module = "core.domain." + package_path
        model = importlib.import_module(model_module)
        models.extend(
            [
                obj
                for _, obj in inspect.getmembers(model)
                if inspect.isclass(obj)
                and issubclass(obj, Model)
                and obj is not Model
                and obj is not signals.Model
                and obj is not BaseEntity
            ]
        )
    return models


from admin.model import Admin

from core.domain.user.user_model import User

user_data = [
    {
        "uid": "ahdwjdtprtm@gmail.com",
        "social_type": "google",
        "nickname": "user1",
        "device_type": "IOS",
        "preference": {
            "alcohols": [1, 2, 3],
            "foods": [13, 22, 4, 12],
        },
    },
    {
        "uid": "iee785@daum.net",
        "social_type": "kakao",
        "nickname": "user2",
        "device_type": "IOS",
    },
    {
        "uid": "tmlee@pluszero.co.kr",
        "social_type": "google",
        "nickname": "user3",
        "device_type": "IOS",
    },
]

from core.domain.feed.feed_model import Feed

feed_data = [
    {
        "user_id": 1,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [1],
        "food_pairing_ids": [14],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
    {
        "user_id": 1,
        "title": "회쏘굳1",
        "content": "회는 굳잡맨 맛나요 짱짱 굳1",
        "alcohol_pairing_ids": [1],
        "food_pairing_ids": [37],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg",
        ],
    },
    {
        "user_id": 2,
        "title": "회쏘굳2",
        "content": "회는 굳잡맨 맛나요 짱짱 굳2",
        "alcohol_pairing_ids": [1],
        "food_pairing_ids": [37],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fb2c56315-9726-4bc4-a7d7-f7d20e303fc1.jpg",
        ],
    },
    {
        "user_id": 3,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [10],
        "food_pairing_ids": [14],
        "user_tags": ["삼겹살은_진리지"],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
    {
        "user_id": 3,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [2],
        "food_pairing_ids": [14],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
    {
        "user_id": 3,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [1, 2],
        "food_pairing_ids": [13, 14],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
    {
        "user_id": 3,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [1, 2],
        "food_pairing_ids": [13, 14],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
    {
        "user_id": 3,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [5],
        "food_pairing_ids": [14, 22],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
    {
        "user_id": 3,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [1, 2],
        "food_pairing_ids": [16, 14],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
    {
        "user_id": 3,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [11],
        "food_pairing_ids": [22, 14],
        "user_tags": ["삼겹살은_진리지"],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
    {
        "user_id": 3,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "alcohol_pairing_ids": [12],
        "food_pairing_ids": [13, 22],
        "user_tags": ["삼겹살은_진리지"],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
]

from core.domain.feed.feed_like_model import FeedLike

feed_like_data = [
    {"user_id": 1, "feed_id": 1},
    {"user_id": 1, "feed_id": 2},
    {"user_id": 2, "feed_id": 1},
    {"user_id": 2, "feed_id": 2},
    {"user_id": 1, "feed_id": 4},
    {"user_id": 1, "feed_id": 5},
]

from core.domain.comment.comment_model import Comment

comment_data = [
    {"user_id": 1, "feed_id": 1, "content": "댓글1", "parent_comment_id": None},
    {"user_id": 1, "feed_id": 1, "content": "댓글2", "parent_comment_id": None},
    {"user_id": 1, "feed_id": 1, "content": "댓글1-1", "parent_comment_id": 1},
    {"user_id": 1, "feed_id": 1, "content": "댓글1-2", "parent_comment_id": 1},
    {"user_id": 1, "feed_id": 1, "content": "댓글1-3", "parent_comment_id": 1},
    {"user_id": 1, "feed_id": 2, "content": "댓글1", "parent_comment_id": None},
    {"user_id": 1, "feed_id": 2, "content": "댓글2", "parent_comment_id": None},
    {"user_id": 1, "feed_id": 2, "content": "댓글1-1", "parent_comment_id": 1},
    {"user_id": 1, "feed_id": 2, "content": "댓글1-2", "parent_comment_id": 1},
    {"user_id": 1, "feed_id": 2, "content": "댓글1-3", "parent_comment_id": 1},
]

from core.domain.pairing.pairing_model import Pairing

pairing_data = [
    {
        "type": "술",
        "subtype": "소주",
        "name": "참이슬",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Ff73cb312-52d4-4a6e-b62c-32fa0d62ea40.png",
        "description": "참이슬입니다",
        "order": 0,
    },
    {
        "type": "술",
        "subtype": "소주",
        "name": "처음처럼",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F23399780-5931-4c8f-92eb-e701bf7875a0.png",
        "description": "처음처럼입니다",
        "order": 1,
    },
    {
        "type": "술",
        "subtype": "소주",
        "name": "진로",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F0464eab9-35a8-44d9-8169-30935821874b.png",
        "description": "진로입니다",
        "order": 2,
    },
    {
        "type": "술",
        "subtype": "소주",
        "name": "좋은데이",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F8b848226-e2e8-4204-99aa-9cf4f1aab186.png",
        "description": "좋은데이입니다",
        "order": 3,
    },
    {
        "type": "술",
        "subtype": "소주",
        "name": "새로",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F3b401b91-ad73-46cd-951d-4d11afc7cf47.png",
        "description": "새로입니다",
        "order": 4,
    },
    {
        "type": "술",
        "subtype": "맥주",
        "name": "카스",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F7d65a3e2-4e24-497f-a57f-b4612091fb46.png",
        "description": "카스입니다",
        "order": 5,
    },
    {
        "type": "술",
        "subtype": "맥주",
        "name": "클라우드",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fad89f34e-c0a8-448b-bb2e-5bbe620e5e0e.png",
        "description": "클라우드입니다",
        "order": 6,
    },
    {
        "type": "술",
        "subtype": "맥주",
        "name": "테라",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fad1ac35f-d14a-47f3-8747-c0ddc8feb384.png",
        "description": "테라입니다",
        "order": 7,
    },
    {
        "type": "술",
        "subtype": "맥주",
        "name": "하이트",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F0cd86be1-fdda-42d6-9585-70d73b60d74b.png",
        "description": "하이트입니다",
        "order": 8,
    },
    {
        "type": "술",
        "subtype": "맥주",
        "name": "오비",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F6d99ce33-d78f-4e3d-9fbe-c49fb8a46431.png",
        "description": "오비입니다",
        "order": 9,
    },
    {
        "type": "술",
        "subtype": "하이볼",
        "name": "하이볼",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F4ef6d21c-6599-46cd-9869-c875bc05edfa.png",
        "description": "하이볼입니다",
        "order": 10,
    },
    {
        "type": "술",
        "subtype": "막걸리",
        "name": "막걸리",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa843352c-4289-4875-9601-e35cd85e72ec.png",
        "description": "막걸리입니다",
        "order": 11,
    },
    {
        "type": "술",
        "subtype": "와인",
        "name": "와인",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa843352c-4289-4875-9601-e35cd85e72ec.png",
        "description": "와인입니다",
        "order": 12,
    },
    {
        "type": "안주",
        "subtype": "패스트푸드",
        "name": "피자",
        "image": None,
        "description": "피자입니다",
    },
    {
        "type": "안주",
        "subtype": "육류",
        "name": "삼겹살",
        "image": None,
        "description": "삼겹살입니다",
    },
    {
        "type": "안주",
        "subtype": "육류",
        "name": "소고기",
        "image": None,
        "description": "소고기입니다",
    },
    {
        "type": "안주",
        "subtype": "육류",
        "name": "족발",
        "image": None,
        "description": "족발입니다",
    },
    {
        "type": "안주",
        "subtype": "육류",
        "name": "육회",
        "image": None,
        "description": "육회입니다",
    },
    {
        "type": "안주",
        "subtype": "육류",
        "name": "곱창",
        "image": None,
        "description": "곱창입니다",
    },
    {
        "type": "안주",
        "subtype": "육류",
        "name": "양꼬치",
        "image": None,
        "description": "양꼬치입니다",
    },
    {
        "type": "안주",
        "subtype": "육류",
        "name": "닭갈비",
        "image": None,
        "description": "닭갈비입니다",
    },
    {
        "type": "안주",
        "subtype": "육류",
        "name": "닭발",
        "image": None,
        "description": "닭발입니다",
    },
    {
        "type": "안주",
        "subtype": "탕류",
        "name": "어묵탕",
        "image": None,
        "description": "어묵탕입니다",
    },
    {
        "type": "안주",
        "subtype": "탕류",
        "name": "짬뽕탕",
        "image": None,
        "description": "짬뽕탕입니다",
    },
    {
        "type": "안주",
        "subtype": "탕류",
        "name": "나가사키 짬뽕",
        "image": None,
        "description": "나가사키 짬뽕입니다",
    },
    {
        "type": "안주",
        "subtype": "튀김류",
        "name": "치킨",
        "image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2F7e0daa65-eca8-4ca9-a922-4c50b40071bf.png",
        "description": "치킨입니다",
    },
    {
        "type": "안주",
        "subtype": "튀김류",
        "name": "감자튀김",
        "image": None,
        "description": "감자튀김입니다",
    },
    {
        "type": "안주",
        "subtype": "튀김류",
        "name": "새우튀김",
        "image": None,
        "description": "새우튀김입니다",
    },
    {
        "type": "안주",
        "subtype": "과일",
        "name": "화채",
        "image": None,
        "description": "화채입니다",
    },
    {
        "type": "안주",
        "subtype": "과일",
        "name": "파인애플",
        "image": None,
        "description": "파인애플입니다",
    },
    {
        "type": "안주",
        "subtype": "과일",
        "name": "황도",
        "image": None,
        "description": "황도입니다",
    },
    {
        "type": "안주",
        "subtype": "과자",
        "name": "나쵸",
        "image": None,
        "description": "나쵸입니다",
    },
    {
        "type": "안주",
        "subtype": "밥류",
        "name": "두부김치",
        "image": None,
        "description": "두부김치입니다",
    },
    {
        "type": "안주",
        "subtype": "밥류",
        "name": "계란말이",
        "image": None,
        "description": "계란말이입니다",
    },
    {
        "type": "안주",
        "subtype": "밥류",
        "name": "국밥",
        "image": None,
        "description": "국밥입니다",
    },
    {
        "type": "안주",
        "subtype": "면류",
        "name": "짜파게티",
        "image": None,
        "description": "짜파게티입니다",
    },
    {"type": "안주", "subtype": "회", "name": "연어", "image": None, "description": "연어입니다"},
    {
        "type": "안주",
        "subtype": "회",
        "name": "광어/우럭",
        "image": None,
        "description": "광어/우럭입니다",
    },
    {
        "type": "안주",
        "subtype": "마른안주",
        "name": "먹태",
        "image": None,
        "description": "먹태입니다",
    },
    {
        "type": "안주",
        "subtype": "마른안주",
        "name": "육포",
        "image": None,
        "description": "육포입니다",
    },
    {
        "type": "안주",
        "subtype": "마른안주",
        "name": "오징어",
        "image": None,
        "description": "오징어입니다",
    },
]

from core.domain.combination.combination_model import Combination

combination_data = [
    {"alcohol": 2, "food": 15, "count": 15469},
    {"alcohol": 13, "food": 16, "count": 5165},
    {"alcohol": 8, "food": 26, "count": 38089},
    {"alcohol": 12, "food": 17, "count": 159},
]

"""
어드민 관련 더미데이터
"""
from core.domain.report.report_model import Report, ReportStatus

reporter_values = [1, 2, 3]
type_values = ["feed", "comment"]
target_id_values = [1, 2, 3]
reason_values = ["욕설", "도배", "광고"]
status_values = [ReportStatus.PENDING.value, ReportStatus.SOLVED.value]

num_reports = 20

report_data = [
    {
        "reporter": random.choice(reporter_values),
        "type": random.choice(type_values),
        "target_id": random.choice(target_id_values),
        "reason": random.choice(reason_values),
        "status": random.choice(status_values),
    }
    for _ in range(num_reports)
]

# 더미데이터 생성용. 더미데이터 생성을 하고 싶으면 주석을 풀고 db_init_tables.py를 실행
db.connect()

# Feed의 FK때문에 선언 순서가 중요함. FeedLike -> Comment -> Feed 순
models = [Admin, User, FeedLike, Comment, Feed, Pairing, Combination, Report]

# db.drop_tables(models, cascade=True)
# db.create_tables(models, safe=True)

# User.bulk_create([User(**data) for data in user_data])
# Feed.bulk_create([Feed(**data) for data in feed_data])
# FeedLike.bulk_create([FeedLike(**data) for data in feed_like_data])
# Comment.bulk_create([Comment(**data) for data in comment_data])
# Pairing.bulk_create([Pairing(**data) for data in pairing_data])
# Combination.bulk_create([Combination(**data) for data in combination_data])
# Report.bulk_create([Report(**data) for data in report_data])

db.close()
