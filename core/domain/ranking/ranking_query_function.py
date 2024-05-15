from datetime import datetime

from peewee import fn, SQL

from core.domain.feed.feed_model import Feed
from core.domain.feed.feed_like_model import FeedLike


def fetch_like_counts_group_by_combination(
    order_by_popular: bool = True, 
    limit: int = 3, 
    start_date = datetime.now(),
    end_date = datetime.now(),
    execute = True,
):
    query = (
        Feed.select(
            fn.ARRAY_CAT(Feed.alcohol_pairing_ids, Feed.food_pairing_ids).alias(
                "combined_ids"
            ),
            fn.COUNT(FeedLike.id).alias("like_count"),
        )
        .where(Feed.created_at >= start_date and Feed.created_at <= end_date)
        .join(FeedLike, on=(Feed.id == FeedLike.feed_id))
        .group_by(SQL("combined_ids"))
        .order_by(SQL("like_count").desc() if order_by_popular else fn.RANDOM())
        .limit(limit)
    )
    return query.execute() if execute else query


def fetch_like_counts_group_by_alcohol(
    limit: int = 10,
    start_date = datetime.now(),
    end_date = datetime.now(),
    execute = True,
):
    query = (
        Feed.select(
            fn.unnest(Feed.alcohol_pairing_ids).alias("alcohol_id"),
            fn.count(Feed.id).alias("like_count"),
        )
        .join(FeedLike, on=(Feed.id == FeedLike.feed_id))
        .group_by(SQL("alcohol_id"))
        .order_by(SQL("like_count").desc())
        .limit(limit)
        # Feed.select(
        #     fn.unnest(Feed.alcohol_pairing_ids).alias("tag"),
        #     fn.count(Feed.id).alias("tag_count"),
        # )
        # .where(Feed.created_at.between(lo=start, hi=end))
        # .group_by(fn.unnest(Feed.alcohol_pairing_ids).alias("tag"))
    )
    return query.execute() if execute else query
