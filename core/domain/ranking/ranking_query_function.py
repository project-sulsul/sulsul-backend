from peewee import fn, SQL

from core.domain.feed.feed_model import Feed
from core.domain.feed.feed_like_model import FeedLike


def fetch_like_counts_group_by_combination(
    order_by_popular: bool = True, limit: str = 3
):
    query = (
        Feed.select(
            fn.ARRAY_CAT(Feed.alcohol_pairing_ids, Feed.food_pairing_ids).alias(
                "combined_ids"
            ),
            fn.COUNT(FeedLike.id).alias("like_count"),
        )
        .join(FeedLike, on=(Feed.id == FeedLike.feed_id))
        .group_by(SQL("combined_ids"))
        .order_by(SQL("like_count").desc() if order_by_popular else fn.RANDOM())
        .limit(limit)
    )
    return query.execute()


def fetch_like_counts_group_by_alcohol():
    query = (
        Feed.select(
            fn.unnest(Feed.alcohol_pairing_ids).alias("alcohol_id"),
            fn.count(Feed.id).alias("like_count"),
        )
        .join(FeedLike, on=(Feed.id == FeedLike.feed_id))
        .group_by(SQL("alcohol_id"))
        .order_by(SQL("like_count").desc())
        # Feed.select(
        #     fn.unnest(Feed.alcohol_pairing_ids).alias("tag"),
        #     fn.count(Feed.id).alias("tag_count"),
        # )
        # .where(Feed.created_at.between(lo=start, hi=end))
        # .group_by(fn.unnest(Feed.alcohol_pairing_ids).alias("tag"))
    )
    return query.execute()
