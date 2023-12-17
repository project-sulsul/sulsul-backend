from typing import List

from pydantic import BaseModel

from core.domain.feed_like_model import FeedLike
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

    @classmethod
    def of(cls, feed: Feed, likes: List[FeedLike], is_liked: bool):
        return FeedResponse(
            feed_id=feed.id,
            writer_info=UserSimpleInfoResponse(
                user_id=feed.user.id,
                nickname=feed.user.nickname,
            ),
            title=feed.title,
            content=feed.content,
            images=feed.images.split(","),
            tags=feed.tags.split(","),
            is_liked=is_liked,
            view_count=feed.view_count,
            likes_count=likes.count(),
        )

    @classmethod
    def from_orm(cls, entity: Feed):
        return FeedResponse(
            id=entity.id,
            writer_user_id=entity.user.id,
            title=entity.title,
            content=entity.content,
            images=entity.images.split(","),
            tags=entity.tags.split(","),
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
