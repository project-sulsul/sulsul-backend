import random
from typing import List

from fastapi import APIRouter, Depends
from peewee import fn
from starlette.requests import Request

from ai.inference import (
    classify,
)
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
    GET_FEEDS_ORDER_BY_FEED_LIKE,
    GET_FEEDS_BY_PREFERENCES_DESC,
    GET_FEEDS_BY_ALCOHOLS_DESC,
    FEED_LIKE_DESC,
    SEARCH_FEED_DESC,
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
    fetch_all_by_alcohol_ids,
    fetch_feeds_order_by_feed_like_and_cominations,
)
from core.domain.pairing.pairing_model import Pairing
from core.domain.ranking.ranking_query_function import (
    fetch_like_counts_group_by_combination,
)
from core.domain.user.user_model import User
from core.dto.feed_dto import (
    FeedResponse,
    FeedUpdateRequest,
    FeedCreateRequest,
    FeedSoftDeleteResponse,
    RandomFeedListResponse,
    PopularFeedListDto,
    FeedByPreferenceListResponse,
    FeedByAlcoholListResponse,
    FeedByAlcoholResponse,
    ClassificationResponse,
    PairingDto,
    FeedLikeResponse,
    FeedSearchListResponse,
)
from core.dto.page_dto import CursorPageResponse
from core.util.auth_util import (
    get_login_user_id,
    get_login_user_or_none,
    AuthRequired,
    AuthOptional,
)
from core.util.cache import pairing_cache_store
from core.util.feed_util import FeedResponseBuilder, parse_user_tags

router = APIRouter(
    prefix="/feeds",
    tags=["Feed"],
)


@router.post(
    "/classifications",
    response_model=ClassificationResponse,
    description=CLASSIFY_IMAGE_DESC,
)
async def classify_image_by_ai(image_url: str):
    classified_names = classify(image_url)
    alcohols = pairing_cache_store.get_all_by_names(classified_names.alcohols)
    foods = pairing_cache_store.get_all_by_names(classified_names.foods)
    return ClassificationResponse(
        alcohols=[PairingDto(id=alcohol.id, name=alcohol.name) for alcohol in alcohols],
        foods=[PairingDto(id=food.id, name=food.name) for food in foods],
    )


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
    "/search",
    dependencies=[Depends(read_only)],
    description=SEARCH_FEED_DESC,
    response_model=FeedSearchListResponse,
)
async def search_feeds(keyword: str):
    keyword = keyword.strip()
    feeds = (
        Feed.select()
        .where(
            Feed.title.contains(keyword) | Feed.content.contains(keyword),
            Feed.is_deleted == False,
        )
        .limit(15)
    )
    return FeedSearchListResponse.of(feeds)


@router.get(
    path="/popular",
    dependencies=[Depends(read_only), Depends(AuthOptional())],
    response_model=List[PopularFeedListDto],
    description=GET_FEEDS_ORDER_BY_FEED_LIKE,
)
async def get_feeds_order_by_feed_like(request: Request, order_by_popular: bool = True):
    # TODO 나중에 배치에서 만든 테이블에 쿼리하도록
    comb_ids_list = []
    for row in fetch_like_counts_group_by_combination(
        order_by_popular=order_by_popular, limit=3
    ):
        comb_ids_list.append(row.combined_ids)
    data = []
    for idx, comb_ids in enumerate(comb_ids_list):
        data.append(
            PopularFeedListDto(
                title=f"{idx + 1}번쨰",
                feeds=[
                    row
                    for row in fetch_feeds_order_by_feed_like_and_cominations(
                        combination_ids=comb_ids, order_by_popular=order_by_popular
                    )
                ],
            )
        )

    return data


@router.get(
    path="/by-preferences",
    dependencies=[Depends(read_only), Depends(AuthRequired())],
    response_model=FeedByPreferenceListResponse,
    description=GET_FEEDS_BY_PREFERENCES_DESC,
)
async def get_feeds_by_preferences(request: Request):
    def get_randomly(pairings: List[int]) -> List[int]:
        return random.sample(pairings, random.randint(1, len(pairings)))

    size = 5
    login_user = User.get_or_raise(get_login_user_id(request))
    random_feeds = [
        feed
        for feed in Feed.select(Feed.is_deleted == False)
        .order_by(fn.Random())
        .limit(size * 2)
    ]  # 넉넉하게 size 2배만큼 랜덤 피드를 가져온다

    alcohols = get_randomly(login_user.preference["alcohols"])
    foods = get_randomly(login_user.preference["foods"])
    feeds_by_preferences = [
        feed
        for feed in Feed.select()
        .where(
            (
                Feed.alcohol_pairing_ids.contains_any(alcohols)
                | Feed.food_pairing_ids.contains_any(foods)
            ),
            Feed.is_deleted == False,
        )
        .order_by(fn.Random())
        .limit(size)
    ]

    if len(feeds_by_preferences) < size:  # 만약 취향으로 가져온 피드 size보다 적으면 나머지는 랜덤피드로 채워넣는다
        feeds_by_preferences.extend(random_feeds[: size - len(feeds_by_preferences)])

    return FeedByPreferenceListResponse.of(feeds_by_preferences)


# TODO : 쿼리 최적화
@router.get(
    path="/by-alcohols",
    dependencies=[Depends(read_only)],
    response_model=FeedByAlcoholListResponse,
    description=GET_FEEDS_BY_ALCOHOLS_DESC,
)
async def get_feeds_by_alcohols():
    alcohols = (
        Pairing.select(Pairing.subtype, fn.array_agg(Pairing.id).alias("ids"))
        .where(Pairing.type == "술")
        .group_by(Pairing.subtype)
    )
    alcohol_ids_dict = {
        alcohol.subtype: [i for i in alcohol.ids] for alcohol in alcohols
    }
    size = 5

    total_feeds = []
    for subtype, alcohol_ids in alcohol_ids_dict.items():
        feeds = []
        for feed in fetch_all_by_alcohol_ids(alcohol_ids, size):
            food_names = pairing_cache_store.get_all_names_by_ids(feed.food_pairing_ids)
            feeds.append(FeedByAlcoholResponse.of(subtype, feed, food_names))
        total_feeds.extend(feeds)
    # 정렬 순서 때문에 하드코딩
    alcohol_subtypes = ["소주", "맥주", "막걸리", "하이볼", "와인"]

    return FeedByAlcoholListResponse.of(total_feeds, alcohol_subtypes)


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
        is_liked=any(like.user.id == login_user.id for like in likes)
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
    request_body.validate_input()
    feed = Feed.create(
        user=login_user,
        title=request_body.title,
        content=request_body.content,
        represent_image=request_body.represent_image,
        images=request_body.images,
        score=request_body.score,
        alcohol_pairing_ids=sorted(request_body.alcohol_pairing_ids),
        food_pairing_ids=sorted(request_body.food_pairing_ids),
        user_tags=parse_user_tags(request_body.user_tags_raw_string),
    )
    return FeedResponse.from_orm(feed).model_dump()


@router.put(
    "/{feed_id}",
    dependencies=[Depends(transactional)],
    response_model=FeedResponse,
    description=UPDATE_FEED_DESC,
)
async def update_feed(request: Request, feed_id: int, request_body: FeedUpdateRequest):
    login_user_id = get_login_user_id(request)
    request_body.validate_input()
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


@router.post(
    "/{feed_id}/like",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=FeedLikeResponse,
    description=FEED_LIKE_DESC,
    responses={**UNAUTHORIZED_RESPONSE, **NOT_FOUND_RESPONSE, **FORBIDDEN_RESPONSE},
)
async def like_feed(request: Request, feed_id: int):
    feed: Feed = Feed.get_or_raise(feed_id)
    login_user_id = get_login_user_id(request)
    feed_like: FeedLike = FeedLike.get_or_none(user=login_user_id, feed=feed)

    if feed_like is None:
        FeedLike.create(user=login_user_id, feed=feed)
        is_liked = True
    else:
        feed_like.delete().where(
            FeedLike.user == login_user_id, FeedLike.feed == feed
        ).execute()
        is_liked = False

    return FeedLikeResponse.of(feed.id, is_liked)
