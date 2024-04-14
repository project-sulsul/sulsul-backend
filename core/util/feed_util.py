from typing import List, Optional

from core.domain.feed.feed_model import Feed
from core.domain.feed.feed_query_function import fetch_feeds_likes_to_dict
from core.domain.user.user_model import User
from core.dto.feed_dto import RelatedFeedResponse
from core.dto.page_dto import CursorPageResponse
from core.util.logger import logger


class FeedResponseBuilder:
    @staticmethod
    def related_feeds(feeds: List[Feed], size: int, login_user: Optional[User] = None):
        likes = fetch_feeds_likes_to_dict(feeds, login_user=login_user)
        is_liked_dict = {
            feed.id: any(like["feed"] == feed.id for like in likes) for feed in feeds
        }
        print(f"likes: {likes}")

        feeds_response = [
            RelatedFeedResponse.of(feed, is_liked_dict[feed.id]) for feed in feeds
        ]
        print(f"feeds_response: {feeds_response}")

        return CursorPageResponse(
            content=feeds_response,
            next_cursor_id=feeds_response[-1].feed_id
            if len(feeds_response) > 0
            else None,
            size=size,
            is_last=len(feeds_response) < size,
        )


def parse_user_tags(user_tags_raw_string: Optional[str]) -> Optional[List[str]]:
    if user_tags_raw_string is None:
        return None

    user_tags = []
    for tag in user_tags_raw_string.split(" "):
        if tag.startswith("#"):
            user_tags.append(tag)

    return user_tags if len(user_tags) != 0 else None
