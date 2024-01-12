from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request
from peewee import fn

from api.descriptions.ranking_api_descriptions import GET_TAGS_RELATED_FEEDS_DESC
from core.config.orm_config import read_only
from core.config.var_config import DEFAULT_PAGE_SIZE, KST
from core.domain.pairing.pairing_query_function import fetch_pairings_by_multiple_ids
from core.domain.ranking.ranking_query_function import fetch_like_counts_group_by_combination
from core.domain.feed.feed_model import Feed
from core.domain.feed.feed_query_function import (
    fetch_related_feeds_by_classify_tags,
)
from core.dto.pairing_dto import PairingResponse
from core.dto.ranking_dto import CombinationRankResponse, CombinationRankingResponse
from core.dto.page_dto import CursorPageResponse
from core.util.auth_util import get_login_user_or_none, AuthRequired, AuthOptional
from core.util.feed_util import FeedResponseBuilder

router = APIRouter(
    prefix="/ranks",
    tags=["Ranking"],
)


@router.get(
    path="/combinations",
    dependencies=[Depends(read_only), Depends(AuthOptional())],
    response_model=CombinationRankingResponse,
)
async def get_combination_ranking(request: Request, order_by_popular: bool = True):
    # TODO 현재는 라이브 쿼리로 가져오나 이후에는 배치에서 랭킹 테이블을 업데이트하고 해당 테이블에 쿼리하는 방식으로 변경
    data = []
    pairing_ids = set()
    for row in fetch_like_counts_group_by_combination(
        order_by_popular=order_by_popular
    ): 
        data.append(row.combined_ids)
        pairing_ids.update(row.combined_ids)
    
    pairings_dict = {pairing.id: pairing for pairing in fetch_pairings_by_multiple_ids(pairing_ids=pairing_ids)}

    ranking_response = CombinationRankingResponse()
    for idx, pairing_ids in enumerate(data):
        rank_response = CombinationRankResponse(rank=idx + 1)
        for pairing_id in pairing_ids:
            rank_response.pairings.append(PairingResponse.from_orm(pairings_dict[pairing_id]))
        ranking_response.ranking.append(rank_response)
    
    return ranking_response


@router.get(
    path="/alcohol",
    dependencies=[Depends(read_only), Depends(AuthOptional())],
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
