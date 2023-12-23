from typing import Optional, List

from peewee import ModelSelect, fn

from core.domain.feed_like_model import FeedLike
from core.domain.feed_model import Feed
from core.domain.user_model import User


def fetch_related_feeds(
    feed_id: int, next_feed_id: Optional[int], size: int
) -> List[Feed]:
    feed = Feed.get_by_id(feed_id)
    return (
        Feed.select()
        .where(
            Feed.tags.contains(feed.tags),
            Feed.id != feed_id,
            Feed.is_deleted == False,
            (
                Feed.id > next_feed_id
                if next_feed_id > 0 or next_feed_id is not None
                else None
            ),
        )
        .order_by(Feed.id.asc())
        .limit(size)
    )


def fetch_related_feeds_likes_to_dict(
    related_feeds: List[Feed], login_user: Optional[User]
) -> dict:
    if login_user is None:
        return {}
    return (
        FeedLike.select()
        .where(
            FeedLike.feed.in_(related_feeds),
            FeedLike.user == login_user.id,
            FeedLike.is_deleted == False,
        )
        .dicts()
    )
