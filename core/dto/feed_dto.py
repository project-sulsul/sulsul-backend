from typing import List

from pydantic import BaseModel

from core.domain.feed_model import Feed


class FeedResponse(BaseModel):
    id: int
    writer_user_id: int
    title: str
    content: str
    images: List[str]
    tags: List[str]

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
