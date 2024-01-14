from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from core.domain.feed.feed_model import Feed
from core.dto.user_dto import UserSimpleInfoResponse


class FeedCreateRequest(BaseModel):
    title: str
    content: str
    represent_image: str
    images: List[str]
    alcohol_pairing_ids: List[int]
    food_pairing_ids: List[int]
    user_tags_raw_string: Optional[str]
    score: float


class FeedResponse(BaseModel):
    feed_id: int
    writer_info: UserSimpleInfoResponse
    title: str
    content: str
    represent_image: str
    images: List[str]
    alcohol_pairing_ids: List[int]
    food_pairing_ids: List[int]
    user_tags: Optional[List[str]]
    is_liked: bool = False
    view_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    score: float
    created_at: datetime
    updated_at: datetime

    @classmethod
    def of(cls, feed: Feed, likes_count: int, comments_count: int, is_liked: bool):
        return FeedResponse(
            **feed.__data__,
            feed_id=feed.id,
            writer_info=UserSimpleInfoResponse(
                user_id=feed.user.id, **feed.user.__data__
            ),
            is_liked=is_liked,
            likes_count=likes_count,
            comments_count=comments_count,
        )

    @classmethod
    def from_orm(cls, feed: Feed):
        return FeedResponse(
            **feed.__data__,
            feed_id=feed.id,
            writer_info=UserSimpleInfoResponse(
                user_id=feed.user.id, **feed.user.__data__
            ),
        )


class FeedUpdateRequest(BaseModel):
    title: Optional[str]
    content: Optional[str]
    images: Optional[List[str]]
    user_tags: Optional[List[str]]


class FeedSearchResultResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]

    @classmethod
    def from_orm(cls, feed: Feed):
        return FeedSearchResultResponse(**feed.__data__)


class FeedSearchResultListResponse(BaseModel):
    keyword: str
    results: List[FeedSearchResultResponse]


class FeedSoftDeleteResponse(BaseModel):
    feed_id: int
    is_deleted: bool
    deleted_comments_count: int
    deleted_likes_count: int

    @classmethod
    def of(cls, feed: Feed, deleted_comments_count: int, deleted_likes_count: int):
        return FeedSoftDeleteResponse(
            feed_id=feed.id,
            is_deleted=feed.is_deleted,
            deleted_comments_count=deleted_comments_count,
            deleted_likes_count=deleted_likes_count,
        )


class RelatedFeedResponse(BaseModel):
    feed_id: int
    title: str
    represent_image: str
    score: float
    user_tags: Optional[List[str]]
    classify_tags: List[str]
    is_liked: bool = False

    @classmethod
    def of(cls, feed: Feed, is_liked: bool):
        return RelatedFeedResponse(
            **feed.__data__,
            feed_id=feed.id,
            is_liked=is_liked,
        )


class RandomFeedDto(BaseModel):
    feed_id: int
    title: str
    content: str
    represent_image: str
    user_id: int
    user_nickname: str
    user_image: Optional[str]
    comments_count: int
    likes_count: int
    updated_at: datetime
    is_liked: bool = False

    def __eq__(self, other):
        return self.feed_id == other.feed_id


class RandomFeedListResponse(BaseModel):
    ids_list: List[int]
    ids_string: str
    feeds: List["RandomFeedDto"]

    @classmethod
    def of_query_dto(cls, feeds: List["RandomFeedDto"]):
        return RandomFeedListResponse(
            ids_list=[feed.feed_id for feed in feeds],
            ids_string=",".join([str(feed.feed_id) for feed in feeds]),
            feeds=feeds,
        )


class PopularFeedDto(BaseModel):
    feed_id: int
    title: str
    content: str
    represent_image: str
    user_id: int
    user_nickname: str
    user_image: Optional[str]
    like_count: int
    created_at: datetime
    updated_at: datetime


class PopularFeedListResponse(BaseModel):
    feeds: List[PopularFeedDto] = []


class FeedByPreferenceResponse(BaseModel):
    feed_id: int
    title: str
    represent_image: str
    score: float
    alcohol_pairing_ids: List[int]
    food_pairing_ids: List[int]
    writer_nickname: str

    @classmethod
    def of(cls, feed: Feed):
        return FeedByPreferenceResponse(
            feed_id=feed.id,
            **feed.__data__,
            writer_nickname=feed.user.nickname,
        )


class FeedByPreferenceListResponse(BaseModel):
    using_preference: bool
    feeds: List[FeedByPreferenceResponse] = []

    @classmethod
    def of(cls, feeds: List[Feed], using_preference: bool):
        return FeedByPreferenceListResponse(
            using_preference=using_preference,
            feeds=sorted([FeedByPreferenceResponse.of(feed) for feed in feeds], key=lambda x: x.score, reverse=True)
        )
