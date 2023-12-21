from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.domain.feed_model import Feed
from core.dto.user_dto import UserSimpleInfoResponse


class FeedResponse(BaseModel):
    feed_id: int
    writer_info: UserSimpleInfoResponse
    title: str
    content: str
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
            **feed.__data__,  # feed 엔티티의 모든 필드를 일단 매핑
            feed_id=feed.id,
            writer_info=UserSimpleInfoResponse(
                user_id=feed.user.id,
                nickname=feed.user.nickname,
                image=feed.user.image,
            ),
            is_liked=is_liked,
            likes_count=likes_count,
            comments_count=comments_count,
        )

    @classmethod
    def from_orm(cls, entity: Feed):
        return FeedResponse(
            id=entity.id,
            writer_user_id=entity.user.id,
            title=entity.title,
            content=entity.content,
            images=entity.images,
            tags=entity.tags,
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
    def from_orm(cls, entity: Feed):
        return FeedSearchResultResponse(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            tags=entity.tags.split(","),
        )


class FeedSearchResultListResponse(BaseModel):
    keyword: str
    results: List[FeedSearchResultResponse]
