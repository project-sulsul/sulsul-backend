from typing import Optional, List

from peewee import fn, Case

from core.domain.comment.comment_model import Comment
from core.domain.feed.feed_like_model import FeedLike
from core.domain.feed.feed_model import Feed
from core.domain.user.user_model import User
from core.dto.feed_dto import RandomFeedDto


def fetch_related_feeds_by_feed_id(
    feed_id: int, next_feed_id: int, size: int
) -> List[Feed]:
    feed = Feed.get_or_raise(feed_id)
    return (
        Feed.select()
        .where(
            (
                Feed.user_tags.contains(feed.user_tags)
                | Feed.classify_tags.contains(feed.classify_tags)
            ),
            Feed.id != feed_id,
            Feed.is_deleted == False,
            Feed.id > next_feed_id,
        )
        .order_by(Feed.id.asc())
        .limit(size)
    )


def fetch_related_feeds_by_classify_tags(
    tags: List[str], next_feed_id: int, size: int
) -> List[Feed]:
    return (
        Feed.select()
        .where(
            Feed.classify_tags.contains(tags),
            Feed.id > next_feed_id,
            Feed.is_deleted == False,
        )
        .order_by(Feed.id)
        .limit(size)
    )


def fetch_feeds_likes_to_dict(
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


def fetch_my_feeds(login_user_id: int, next_feed_id: int, size: int) -> List[Feed]:
    return (
        Feed.select()
        .where(
            Feed.user == login_user_id,
            Feed.is_deleted == False,
            Feed.id > next_feed_id,
        )
        .limit(size)
        .order_by(Feed.id.asc())
    )


def fetch_feeds_liked_by_me(
    login_user_id: int, next_feed_id: int, size: int
) -> List[Feed]:
    return (
        Feed.select()
        .join(FeedLike)
        .where(
            FeedLike.user == login_user_id,
            FeedLike.is_deleted == False,
            Feed.is_deleted == False,
            Feed.id > next_feed_id,
        )
        .limit(size)
        .order_by(Feed.id.asc())
    )


def fetch_feeds_randomly(
    size: int, exclude_feed_ids: List[int], login_user_id: Optional[int] = None
) -> List[RandomFeedDto]:
    projection_fields = [
        Feed.id.alias("feed_id"),
        Feed.title,
        Feed.content,
        Feed.represent_image,
        Feed.updated_at,
        User.id.alias("user_id"),
        User.nickname.alias("user_nickname"),
        User.image.alias("user_image"),
        fn.Count(Comment.id).alias("comments_count"),
        fn.Count(FeedLike.id).alias("likes_count"),
    ]
    feed_like_join_condition = FeedLike.feed == Feed.id
    if login_user_id is not None:
        projection_fields.append(
            Case(None, [(FeedLike.user == login_user_id, True)], False).alias(
                "is_liked"
            ),
        )
        feed_like_join_condition = (FeedLike.feed == Feed.id) & (
            FeedLike.user == login_user_id
        )

    return (
        Feed.select(*projection_fields)
        .left_outer_join(FeedLike, on=feed_like_join_condition)
        .left_outer_join(Comment, on=(Comment.feed == Feed.id))
        .join(User, on=(User.id == Feed.user))
        .where(
            Feed.is_deleted == False,
            (
                (Comment.is_deleted == False) | (Comment.is_deleted.is_null())
            ),  # 댓글이 없는 경우도 카운트하기 위함
            Feed.id.not_in(exclude_feed_ids),
        )
        .group_by(Feed.id, User.id, FeedLike.id)
        .limit(size)
        .order_by(fn.Random())
        .objects(constructor=RandomFeedDto)
    )
