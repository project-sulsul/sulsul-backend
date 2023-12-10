from pydantic import BaseModel

from core.domain.feed_model import Feed


class FeedResponse(BaseModel):
    id: int

    @classmethod
    def from_orm(cls, entity: Feed):
        return FeedResponse(
            id=entity.id,
        )


class FeedUpdateRequest(BaseModel):
    content: str
