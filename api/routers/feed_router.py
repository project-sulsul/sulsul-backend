from fastapi import APIRouter, Depends
from starlette.requests import Request

from ai.inference import classify, ClassificationResultDto
from api.descriptions.feed_api_descriptions import (
    GET_RELATED_FEEDS_DESC,
    DELETE_FEED_DESC,
    GET_RANDOM_FEEDS_DESC,
    GET_FEEDS_LIKED_BY_ME_DESC,
    GET_FEEDS_BY_ME_DESC,
    CLASSIFY_IMAGE_DESC,
    CREATE_FEED_DESC,
    GET_FEED_DESC,
    UPDATE_FEED_DESC,
)
from api.descriptions.responses_dict import (
    UNAUTHORIZED_RESPONSE,
    NOT_FOUND_RESPONSE,
    FORBIDDEN_RESPONSE,
)
from core.config.orm_config import transactional, read_only
from core.config.var_config import DEFAULT_PAGE_SIZE
from core.domain.comment.comment_model import Comment
from core.domain.feed.feed_like_model import FeedLike
from core.domain.feed.feed_model import Feed
from core.domain.feed.feed_query_function import (
    fetch_related_feeds_by_feed_id,
    fetch_feeds_liked_by_me,
    fetch_my_feeds,
    fetch_feeds_randomly,
)
from core.domain.user.user_model import User
from core.dto.feed_dto import (
    FeedResponse,
    FeedUpdateRequest,
    FeedCreateRequest,
    FeedSoftDeleteResponse,
    RandomFeedListResponse,
)
from core.dto.page_dto import CursorPageResponse
from core.util.auth_util import (
    get_login_user_id,
    get_login_user_or_none,
    AuthRequired,
    AuthOptional,
)
from core.util.feed_util import FeedResponseBuilder

router = APIRouter(
    prefix="/feeds",
    tags=["Feed"],
)


@router.post(
    "/classifications",
    response_model=ClassificationResultDto,
    description=CLASSIFY_IMAGE_DESC,
)
async def classify_image_by_ai(image_url: str):
    return classify(image_url)


@router.get(
    "/by-me",
    dependencies=[Depends(read_only), Depends(AuthRequired())],
    response_model=CursorPageResponse,
    description=GET_FEEDS_BY_ME_DESC,
    responses=UNAUTHORIZED_RESPONSE,
)
async def get_all_my_feeds(
    request: Request, next_feed_id: int = 0, size: int = DEFAULT_PAGE_SIZE
):
    my_feeds = fetch_my_feeds(get_login_user_id(request), next_feed_id, size)
    return CursorPageResponse.of_feeds(my_feeds)


@router.get(
    "/liked-by-me",
    dependencies=[Depends(read_only), Depends(AuthRequired())],
    response_model=CursorPageResponse,
    description=GET_FEEDS_LIKED_BY_ME_DESC,
    responses=UNAUTHORIZED_RESPONSE,
)
async def get_all_liked_feeds_by_me(
    request: Request, next_feed_id: int = 0, size: int = DEFAULT_PAGE_SIZE
):
    feeds_liked_by_me = fetch_feeds_liked_by_me(
        get_login_user_id(request), next_feed_id, size
    )
    return CursorPageResponse.of_feeds(feeds_liked_by_me)


@router.get(
    "/random",
    dependencies=[Depends(read_only), Depends(AuthOptional())],
    response_model=RandomFeedListResponse,
    description=GET_RANDOM_FEEDS_DESC,
)
async def get_random_feeds(
    request: Request,
    exclude_feed_ids: str = "",  # separated by comma ex. 1,2,3
    size: int = DEFAULT_PAGE_SIZE,
):
    exclude_feed_ids = [int(i) for i in exclude_feed_ids.split(",") if i != ""]
    random_feeds = fetch_feeds_randomly(
        size, exclude_feed_ids, get_login_user_id(request)
    )
    return RandomFeedListResponse.of_query_dto(random_feeds)


@router.get(
    "/{feed_id}",
    dependencies=[Depends(transactional), Depends(AuthOptional())],
    response_model=FeedResponse,
    description=GET_FEED_DESC,
    responses=NOT_FOUND_RESPONSE,
)
async def get_feed_by_id(request: Request, feed_id: int):
    login_user = User.get_or_none(get_login_user_id(request))
    feed = Feed.get_or_raise(feed_id)
    likes = FeedLike.select().where(FeedLike.feed == feed)
    comments_count = (
        Comment.select()
        .where(Comment.feed == feed, Comment.is_deleted == False)
        .count()
    )

    feed.add_view_count()

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
    dependencies=[Depends(read_only), Depends(AuthOptional())],
    response_model=CursorPageResponse,
    description=GET_RELATED_FEEDS_DESC,
    responses=NOT_FOUND_RESPONSE,
)
async def get_related_feeds(
    request: Request, feed_id: int, next_feed_id: int = 0, size: int = DEFAULT_PAGE_SIZE
):
    return FeedResponseBuilder.related_feeds(
        feeds=fetch_related_feeds_by_feed_id(feed_id, next_feed_id, size),
        size=size,
        login_user=get_login_user_or_none(request),
    )


@router.post(
    "",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=FeedResponse,
    description=CREATE_FEED_DESC,
    responses={**NOT_FOUND_RESPONSE, **UNAUTHORIZED_RESPONSE},
)
async def create_feed(request: Request, request_body: FeedCreateRequest):
    login_user = User.get_or_raise(get_login_user_id(request))
    feed = Feed.create(
        user=login_user,
        title=request_body.title,
        content=request_body.content,
        represent_image=request_body.represent_image,
        images=request_body.images,
        score=request_body.score,
        classify_tags=request_body.classify_tags,
        user_tags=request_body.user_tags,
    )
    return FeedResponse.from_orm(feed).model_dump()


@router.put(
    "/{feed_id}",
    dependencies=[Depends(transactional)],
    response_model=FeedResponse,
    description=UPDATE_FEED_DESC,
)
@auth_required
async def update_feed(request: Request, feed_id: int, request_body: FeedUpdateRequest):
    login_user_id = get_login_user_id(request)
    feed = Feed.get_or_raise(feed_id)
    feed.check_if_owner(login_user_id)
    feed.update_feed(
        request_body.title,
        request_body.content,
        request_body.images,
        request_body.user_tags,
    )
    return FeedResponse.from_orm(feed).model_dump()


@router.delete(
    "/{feed_id}",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=FeedSoftDeleteResponse,
    description=DELETE_FEED_DESC,
    responses={**UNAUTHORIZED_RESPONSE, **NOT_FOUND_RESPONSE, **FORBIDDEN_RESPONSE},
)
async def soft_delete_feed(request: Request, feed_id: int):
    feed: Feed = Feed.get_or_raise(feed_id)
    feed.check_if_owner(get_login_user_id(request))

    feed.soft_delete()
    deleted_comment_count = (
        Comment.update(is_deleted=True).where(Comment.feed == feed).execute()
    )
    deleted_likes_count = FeedLike.delete().where(FeedLike.feed == feed).execute()

    return FeedSoftDeleteResponse.of(feed, deleted_comment_count, deleted_likes_count)
