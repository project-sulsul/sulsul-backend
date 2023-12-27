import os, inspect, importlib
from peewee import Model
from playhouse import signals

from core.config.orm_config import db
from core.domain.base_entity import BaseEntity

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
            and obj is not BaseEntity
        ]
    )

db.connect()

from admin.model import Admin

db.create_tables([Admin], safe=True)

db.drop_tables(models, cascade=True)
db.create_tables(models)

from core.domain.user_model import User

user_data = [
    {"uid": "ahdwjdtprtm@gmail.com", "social_type": "google", "nickname": "user1"},
    {"uid": "iee785@daum.net", "social_type": "kakao", "nickname": "user2"},
    {"uid": "tmlee@pluszero.co.kr", "social_type": "google", "nickname": "user3"},
]
User.bulk_create([User(**data) for data in user_data])

from core.domain.feed_model import Feed

feed_data = [
    {
        "user_id": 1,
        "title": "삼쏘굳",
        "content": "삼겹살이 맛나요 짱짱 굳",
        "tags": ["삼겹살", "소주"],
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
        "tags": ["회", "소주"],
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
        "tags": ["회", "소주"],
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
        "tags": ["삼겹살", "소주"],
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
        "tags": ["삼겹살", "소주"],
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
        "tags": ["삼겹살", "소주"],
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
        "tags": ["삼겹살", "소주"],
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
        "tags": ["삼겹살", "소주"],
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
        "tags": ["삼겹살", "소주"],
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
        "tags": ["삼겹살", "소주"],
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
        "tags": ["삼겹살", "소주"],
        "represent_image": "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        "images": [
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
            "https://s3-ap-northeast-2.amazonaws.com/sulsul-s3/images%2Fa1402cd7-2bac-4863-ab71-6df75acfe25f.jpg",
        ],
    },
]
Feed.bulk_create([Feed(**data) for data in feed_data])

from core.domain.feed_like_model import FeedLike

feed_like_data = [
    {"user_id": 1, "feed_id": 1},
    {"user_id": 1, "feed_id": 2},
    {"user_id": 2, "feed_id": 1},
    {"user_id": 2, "feed_id": 2},
    {"user_id": 1, "feed_id": 4},
    {"user_id": 1, "feed_id": 5},
]
FeedLike.bulk_create([FeedLike(**data) for data in feed_like_data])

from core.domain.comment_model import Comment

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
Comment.bulk_create([Comment(**data) for data in comment_data])

from core.domain.pairing_model import Pairing

pairing_data = [
    {
        "type": "술",
        "subtype": "소주",
        "name": "처음처럼",
        "image": "https://company.lottechilsung.co.kr/common/images/product_view0201_bh3.jpg",
        "description": "처음처럼입니다",
    },
    {
        "type": "술",
        "subtype": "소주",
        "name": "참이슬",
        "image": "https://i.namu.wiki/i/ZVfJTwmV_vCcRZNbdsvAGMGvZwiAOOjLrtMWleBZw_OU7ESw598EcldhTBekyA2Xu93s711gVFA7-avlPgFvuG--xRqH5deJbh_X47v-dRZcRE3EzyuRnpWF9ZpFDdoGewaPBaaeqBuL5tKeoP3q4Q.webp",
        "description": "참이슬입니다",
    },
    {
        "type": "술",
        "subtype": "소주",
        "name": "좋은데이",
        "image": None,
        "description": "좋은데이입니다",
    },
    {"type": "술", "subtype": "소주", "name": "진로", "image": None, "description": "진로입니다"},
    {"type": "술", "subtype": "소주", "name": "새로", "image": None, "description": "새로입니다"},
    {
        "type": "술",
        "subtype": "맥주",
        "name": "카스",
        "image": "https://i.namu.wiki/i/fKo1mq_4u-VpRRswz6kcdSAMucQy0xlHTk8zVRmw4IP2F4yUKOpSlo68_8ba1W_S76LB9vFjIPWci7XCntq7XimPXMCrbT-q6BSkwevELkZpcDfyxQw7SPe5aRJnY3BxNJdmvASMMsxaYafWRIfDvA.webp",
        "description": "카스입니다",
    },
    {
        "type": "술",
        "subtype": "맥주",
        "name": "클라우드",
        "image": None,
        "description": "클라우드입니다",
    },
    {"type": "술", "subtype": "맥주", "name": "테라", "image": None, "description": "테라입니다"},
    {
        "type": "술",
        "subtype": "맥주",
        "name": "하이트",
        "image": None,
        "description": "하이트입니다",
    },
    {"type": "술", "subtype": "맥주", "name": "오비", "image": None, "description": "오비입니다"},
    {
        "type": "술",
        "subtype": "하이볼",
        "name": "하이볼",
        "image": None,
        "description": "하이볼입니다",
    },
    {
        "type": "술",
        "subtype": "막걸리",
        "name": "막걸리",
        "image": None,
        "description": "막걸리입니다",
    },
    {"type": "술", "subtype": "와인", "name": "와인", "image": None, "description": "와인입니다"},
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
        "image": None,
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
Pairing.bulk_create([Pairing(**data) for data in pairing_data])

from core.domain.combination_model import Combination

combination_data = [
    {"alcohol": 2, "food": 15, "count": 15469},
    {"alcohol": 13, "food": 16, "count": 5165},
    {"alcohol": 8, "food": 26, "count": 38089},
    {"alcohol": 12, "food": 17, "count": 159},
]
Combination.bulk_create([Combination(**data) for data in combination_data])

db.close()
