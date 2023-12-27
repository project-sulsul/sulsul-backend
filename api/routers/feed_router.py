from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from ai.inference import classify, ClassificationResultDto
from api.config.middleware import auth, auth_required, only_mine
from core.config.orm_config import transactional, read_only
from core.config.var_config import DEFAULT_PAGE_SIZE
from core.domain.comment_model import Comment
from core.domain.feed_like_model import FeedLike
from core.domain.feed_model import Feed
from core.domain.feed_query_function import (
    fetch_related_feeds,
    fetch_related_feeds_likes_to_dict,
    fetch_feeds_liked_by_me,
    fetch_my_feeds,
)
from core.domain.user_model import User
from core.dto.feed_dto import (
    FeedResponse,
    FeedUpdateRequest,
    FeedSearchResultListResponse,
    FeedSearchResultResponse,
    FeedCreateRequest,
    FeedSoftDeleteResponse,
    RelatedFeedResponse,
)
from core.dto.page_dto import CursorPageResponse
from core.util.auth_util import get_login_user_id, get_login_user_or_none

router = APIRouter(
    prefix="/feeds",
    tags=["Feed"],
)

from ai.inference import classify, ClassificationResultDto


@router.post(
    "/classifications",
    response_model=ClassificationResultDto,
)
async def classify_image_by_ai(image_url: str):
    return classify(image_url)


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
    "/by-me",
    dependencies=[Depends(read_only)],
    response_model=CursorPageResponse,
)
@auth_required
async def get_all_my_feeds(
    request: Request, next_feed_id: int = 0, size: int = DEFAULT_PAGE_SIZE
):
    my_feeds = fetch_my_feeds(get_login_user_id(request), next_feed_id, size)
    return CursorPageResponse.of_feeds(my_feeds)


@router.get(
    "/liked-by-me",
    dependencies=[Depends(read_only)],
    response_model=CursorPageResponse,
)
@auth_required
async def get_all_liked_feeds_by_me(
    request: Request, next_feed_id: int = 0, size: int = DEFAULT_PAGE_SIZE
):
    feeds_liked_by_me = fetch_feeds_liked_by_me(
        get_login_user_id(request), next_feed_id, size
    )
    return CursorPageResponse.of_feeds(feeds_liked_by_me)


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
        .where(Comment.feed == feed, Comment.is_deleted == False)
        .count()
    )

    return FeedResponse.of(
        feed=feed,
        likes_count=len(likes),
        comments_count=comments_count,
        is_liked=any(like.user == login_user.feed_id for like in likes)
        if login_user is not None
        else False,
    )


@router.get(
    "/{feed_id}/related-feeds",
    dependencies=[Depends(read_only)],
    response_model=CursorPageResponse,
)
@auth
async def get_related_feeds(
    request: Request, feed_id: int, next_feed_id: int = 0, size: int = DEFAULT_PAGE_SIZE
):
    related_feeds = fetch_related_feeds(feed_id, next_feed_id, size)

    likes = fetch_related_feeds_likes_to_dict(
        related_feeds, login_user=get_login_user_or_none(request)
    )
    is_liked_dict = {
        feed.id: any(like["feed"] == feed.id for like in likes)
        for feed in related_feeds
    }

    related_feeds_response = [
        RelatedFeedResponse.of(feed, is_liked_dict[feed.id]) for feed in related_feeds
    ]

    return CursorPageResponse(
        content=related_feeds_response,
        next_cursor_id=related_feeds_response[-1].feed_id
        if len(related_feeds_response) > 0
        else None,
        size=size,
        is_last=len(related_feeds_response) < size,
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


@router.delete(
    "/{feed_id}",
    dependencies=[Depends(transactional)],
    response_model=FeedSoftDeleteResponse,
)
@auth_required
@only_mine  # TODO 삭제예정
async def soft_delete_feed(request: Request, feed_id: int):
    feed = Feed.get_by_id(feed_id)

    Feed.update(is_deleted=True).where(Feed.id == feed_id).execute()
    deleted_comment_count = (
        Comment.update(is_deleted=True).where(Comment.feed == feed).execute()
    )
    deleted_likes_count = (
        FeedLike.update(is_deleted=True).where(FeedLike.feed == feed).execute()
    )

    return FeedSoftDeleteResponse.of(feed, deleted_comment_count, deleted_likes_count)
