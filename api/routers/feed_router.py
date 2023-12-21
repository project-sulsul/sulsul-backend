from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from ai.inference import classify, ClassificationResultDto
from api.config.exceptions import ForbiddenException
from api.config.middleware import auth, auth_required
from core.config.orm_config import transactional, read_only
from core.domain.comment_model import Comment
from core.domain.feed_like_model import FeedLike
from core.domain.feed_model import Feed
from core.domain.user_model import User
from core.dto.feed_dto import (
    FeedResponse,
    FeedUpdateRequest,
    FeedSearchResultListResponse,
    FeedSearchResultResponse,
    FeedCreateRequest,
    FeedSoftDeleteResponse,
)
from core.util.auth_util import get_login_user_id

router = APIRouter(
    prefix="/feeds",
    tags=["Feed"],
)


# Not used at MVP
@router.get(
    "/search",
    dependencies=[Depends(read_only)],
    response_model=FeedSearchResultListResponse,
)
async def search_feeds(keyword: str):
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
    dependencies=[Depends(read_only)],
    response_model=FeedResponse,
)
@auth
async def get_feed_by_id(request: Request, feed_id: int):
    login_user = User.get_or_none(get_login_user_id(request))
    feed = Feed.get_by_id(feed_id)
    likes = FeedLike.select().where(FeedLike.feed == feed)
    comments_count = (
        Comment.select()
        .where((Comment.feed == feed) & (Comment.is_deleted == False))
        .count()
    )

    return FeedResponse.of(
        feed=feed,
        likes_count=len(likes),
        comments_count=comments_count,
        is_liked=any(like.user == login_user.id for like in likes),
    )


@router.post(
    "",
    dependencies=[Depends(transactional)],
    response_model=FeedResponse,
)
@auth_required
async def create_feed(request: Request, request_body: FeedCreateRequest):
    login_user = User.get_by_id(get_login_user_id(request))
    feed = Feed.create(
        user=login_user,
        title=request_body.title,
        content=request_body.content,
        represent_image=request_body.represent_image,
        images=request_body.images,
        tags=request_body.tags,
    )
    return FeedResponse.from_orm(feed).model_dump()


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


@router.post(
    "/classifications",
    response_model=ClassificationResultDto,
)
async def classify_image_by_ai(image_url: str):
    return classify(image_url)


@router.delete(
    "/{feed_id}",
    dependencies=[Depends(transactional)],
    response_model=FeedSoftDeleteResponse,
)
@auth_required
async def soft_delete_feed(request: Request, feed_id: int):
    login_user = User.get_by_id(get_login_user_id(request))
    feed = Feed.get_by_id(feed_id)

    if feed.user != login_user:
        raise ForbiddenException("You are not the owner of this feed.")

    Feed.update(is_deleted=True).where(Feed.id == feed_id).execute()
    deleted_comment_count = (
        Comment.update(is_deleted=True).where(Comment.feed == feed).execute()
    )
    deleted_likes_count = (
        FeedLike.update(is_deleted=True).where(FeedLike.feed == feed).execute()
    )

    return FeedSoftDeleteResponse.of(feed, deleted_comment_count, deleted_likes_count)
