from fastapi import APIRouter, Depends
from peewee import JOIN
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.config.middleware import auth
from core.config.orm_config import transactional, get_db
from core.domain.comment_model import Comment
from core.domain.feed_like_model import FeedLike
from core.domain.feed_model import Feed
from core.domain.user_model import User
from core.dto.feed_dto import (
    FeedResponse,
    FeedUpdateRequest,
    FeedListResponse,
    FeedSearchResultListResponse,
    FeedSearchResultResponse,
)

router = APIRouter(
    prefix="/feeds",
    tags=["Feed"],
)


@router.get(
    "/search",
    dependencies=[Depends(get_db)],
    response_model=FeedSearchResultListResponse,
)
async def search_feeds(request: Request, keyword: str):
    query_results = Feed.select().where(
        (
            Feed.content.contains(keyword)
            | (Feed.tags.contains(keyword))
            | (Feed.title.contains(keyword))
        )
    )
    data = [
        FeedSearchResultResponse.from_orm(feed).model_dump() for feed in query_results
    ]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=FeedSearchResultListResponse(
            results=data, keyword=keyword
        ).model_dump(),
    )


@router.get(
    "/{feed_id}",
    dependencies=[Depends(get_db)],
    response_model=FeedResponse,
)
@auth
async def get_feed_by_id(request: Request, feed_id: int):
    token_info = request.state.token_info
    login_user = None
    if token_info is not None:
        login_user = User.get_by_id(token_info["id"])
    feed = Feed.get_by_id(feed_id)
    likes = FeedLike.select().where(FeedLike.feed == feed)
    comments_count = Comment.select().where(Comment.feed == feed).count()

    is_liked = False
    for like in likes:
        if like.user == login_user:
            is_liked = True
            break

    return FeedResponse.of(
        feed=feed,
        likes_count=len(likes),
        comments_count=comments_count,
        is_liked=is_liked,
    )


@router.put(
    "/{feed_id}",
    dependencies=[Depends(transactional)],
    response_model=FeedResponse,
)
async def update_feed(request: Request, feed_id: int, request_body: FeedUpdateRequest):
    feed = Feed.get_by_id(feed_id)
    feed.content = request_body.content
    feed.save()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=FeedResponse.from_orm(feed).model_dump()
    )