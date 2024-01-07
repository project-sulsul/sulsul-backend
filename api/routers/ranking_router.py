from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request
from peewee import fn

from api.descriptions.ranking_api_descriptions import GET_TAGS_RELATED_FEEDS_DESC
from core.config.orm_config import read_only
from core.config.var_config import DEFAULT_PAGE_SIZE, KST
from core.domain.combination import combination_query_function
from core.domain.feed.feed_model import Feed
from core.domain.feed.feed_query_function import (
    fetch_related_feeds_by_classify_tags,
)
from core.dto.combination_dto import CombinationResponse, CombinationListResponse
from core.dto.page_dto import CursorPageResponse
from core.util.auth_util import get_login_user_or_none, AuthRequired, AuthOptional
from core.util.feed_util import FeedResponseBuilder

router = APIRouter(
    prefix="/ranks",
    tags=["Ranking"],
)


@router.get(
    path="/combinations",
    dependencies=[Depends(read_only), Depends(AuthRequired())],
    response_model=CombinationListResponse,
)
async def get_combination_ranking(request: Request, order_by_popular: bool = True):
    combinations = [
        CombinationResponse(**record)
        for record in combination_query_function.fetch_combination_ranking(
            order_by_popular
        )
    ]
    return CombinationListResponse(combinations=combinations)


@router.get(
    path="/alcohol",
    dependencies=[Depends(read_only), Depends(AuthRequired())],
    # response_model=
)
async def get_alcohol_ranking(request: Request):
    # 이번 주 기간(금~목)
    today = datetime.now(KST).replace(hour=0, minute=0, second=0, microsecond=0)
    start = today - timedelta(days=today.weekday() + 3)
    end = start + timedelta(days=7)

    query = (
        Feed.select(
            fn.unnest(Feed.classify_tags).alias("tag"),
            fn.count(Feed.id).alias("tag_count"),
        )
        .where(Feed.created_at.between(lo=start, hi=end))
        .group_by(fn.unnest(Feed.classify_tags).alias("tag"))
    )
    return {record.tag: record.tag_count for record in query.execute()}


@router.get(
    path="/related-feeds",
    dependencies=[Depends(read_only), Depends(AuthOptional())],
    response_model=CursorPageResponse,
    description=GET_TAGS_RELATED_FEEDS_DESC,
)
async def get_related_feeds_by_classify_tags(
    request: Request,
    tags: str,  # comma separated tags
    next_feed_id: int = 0,
    size: int = DEFAULT_PAGE_SIZE,
):
    return FeedResponseBuilder.related_feeds(
        feeds=fetch_related_feeds_by_classify_tags(tags.split(","), next_feed_id, size),
        size=size,
        login_user=get_login_user_or_none(request),
    )
