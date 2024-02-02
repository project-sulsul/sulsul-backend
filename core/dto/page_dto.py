from typing import Optional, List

from pydantic import BaseModel

from core.config.var_config import DEFAULT_PAGE_SIZE
from core.domain.feed.feed_model import Feed
from core.dto.feed_dto import FeedResponse, RelatedFeedResponse


class CursorPageResponse(BaseModel):
    next_cursor_id: Optional[int]
    size: int
    is_last: bool
    content: Optional[list]

    @staticmethod
    def of_feeds(feeds: List[Feed]):
        return CursorPageResponse(
            content=[FeedResponse.from_orm(feed).model_dump() for feed in feeds],
            next_cursor_id=feeds[-1].id if len(feeds) > 0 else None,
            size=DEFAULT_PAGE_SIZE,
            is_last=len(feeds) < DEFAULT_PAGE_SIZE,
        )

    @staticmethod
    def of_related_feeds_response(related_feeds_response: List[RelatedFeedResponse]):
        return CursorPageResponse(
            content=related_feeds_response,
            next_cursor_id=related_feeds_response[-1].feed_id
            if len(related_feeds_response) > 0
            else None,
            size=DEFAULT_PAGE_SIZE,
            is_last=len(related_feeds_response) < DEFAULT_PAGE_SIZE,
        )


class NormalPageResponse(BaseModel):
    total_count: int
    size: int
    is_last: bool
    content: list
