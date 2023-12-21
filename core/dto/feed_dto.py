from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.domain.feed_model import Feed
from core.dto.user_dto import UserSimpleInfoResponse


class FeedCreateRequest(BaseModel):
    title: str
    content: str
    represent_image: str
    images: List[str]
    tags: List[str]
    score: float


class FeedResponse(BaseModel):
    feed_id: int
    writer_info: UserSimpleInfoResponse
    title: str
    content: str
    represent_image: str
    images: List[str]
    tags: List[str]
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
    content: str


class FeedListResponse(BaseModel):
    feeds: List[FeedResponse]

    @classmethod
    def from_orm(cls, entities: List[Feed]):
        return FeedListResponse(
            feeds=[FeedResponse.from_orm(entity) for entity in entities]
        )


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
