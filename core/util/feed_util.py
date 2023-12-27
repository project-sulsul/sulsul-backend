from typing import List, Optional

from fastapi import HTTPException
from starlette import status

from core.domain.feed_model import Feed
from core.domain.feed_query_function import fetch_feeds_likes_to_dict
from core.domain.user_model import User
from core.dto.feed_dto import RelatedFeedResponse
from core.dto.page_dto import CursorPageResponse


class FeedValidator:
    @staticmethod
    def check_if_exist(feed_id: int):
        feed = Feed.get_or_none(feed_id)
        if feed is None or feed.is_deleted is True:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"feed(id:{feed_id}) is not found",
            )


class FeedResponseBuilder:
    @staticmethod
    def related_feeds(feeds: List[Feed], size: int, login_user: Optional[User] = None):
        likes = fetch_feeds_likes_to_dict(feeds, login_user=login_user)
        is_liked_dict = {
            feed.id: any(like["feed"] == feed.id for like in likes) for feed in feeds
        }

        feeds_response = [
            RelatedFeedResponse.of(feed, is_liked_dict[feed.id]) for feed in feeds
        ]

        return CursorPageResponse(
            content=feeds_response,
            next_cursor_id=feeds_response[-1].feed_id
            if len(feeds_response) > 0
            else None,
            size=size,
            is_last=len(feeds_response) < size,
        )
