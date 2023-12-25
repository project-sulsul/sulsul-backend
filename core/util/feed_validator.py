from fastapi import HTTPException
from starlette import status

from core.domain.feed_model import Feed


class FeedValidator:
    @staticmethod
    def check_if_exist(feed_id: int):
        feed = Feed.get_or_none(feed_id)
        if feed is None or feed.is_deleted is True:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"feed(id:{feed_id}) is not found",
            )
