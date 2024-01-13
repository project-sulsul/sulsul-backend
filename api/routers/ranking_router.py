from fastapi import APIRouter, Depends, Request

from api.descriptions.ranking_api_descriptions import (
    GET_COMBINATION_RANKING_DESC,
    GET_ALCOHOL_RANKING_DESC,
    GET_TAGS_RELATED_FEEDS_DESC,
)
from core.config.orm_config import read_only
from core.config.var_config import DEFAULT_PAGE_SIZE
from core.domain.pairing.pairing_query_function import fetch_pairings_by_multiple_ids
from core.domain.ranking.ranking_query_function import (
    fetch_like_counts_group_by_combination,
    fetch_like_counts_group_by_alcohol,
)
from core.domain.feed.feed_model import Feed
from core.domain.feed.feed_query_function import (
    fetch_related_feeds_by_classify_tags,
)
from core.dto.pairing_dto import PairingResponse
from core.dto.ranking_dto import (
    CombinationRankResponse,
    CombinationRankingResponse,
    AlcoholRankResponse,
    AlcoholRankingResponse,
)
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
    description=GET_COMBINATION_RANKING_DESC,
)
async def get_combination_ranking(request: Request):
    # TODO 현재는 라이브 쿼리로 가져오나 이후에는 배치를 통해 집계된 데이터 조회하도록 변경
    data = []
    pairing_ids = set()
    for row in fetch_like_counts_group_by_combination(limit=10):
        data.append(row.combined_ids)
        pairing_ids.update(row.combined_ids)

    pairings_dict = {
        pairing.id: pairing
        for pairing in fetch_pairings_by_multiple_ids(pairing_ids=pairing_ids)
    }

    ranking_response = CombinationRankingResponse()
    for idx, pairing_ids in enumerate(data):
        rank_response = CombinationRankResponse(rank=idx + 1)
        for pairing_id in pairing_ids:
            rank_response.pairings.append(
                PairingResponse.from_orm(pairings_dict[pairing_id])
            )
        ranking_response.ranking.append(rank_response)

    return ranking_response


@router.get(
    path="/alcohol",
    dependencies=[Depends(read_only), Depends(AuthOptional())],
    response_model=AlcoholRankingResponse,
    description=GET_ALCOHOL_RANKING_DESC,
)
async def get_alcohol_ranking(request: Request):
    # 이번 주 기간(금~목)
    # TODO 현재는 시간이 없음 이것도 배치로 뺴면서 테이블이랑 시간 필터 만들어야됨
    # today = datetime.now(KST).replace(hour=0, minute=0, second=0, microsecond=0)
    # start = today - timedelta(days=today.weekday() + 3)
    # end = start + timedelta(days=7)

    alcohol_ids = []
    for row in fetch_like_counts_group_by_alcohol():
        alcohol_ids.append(row.alcohol_id)

    alcohols_dict = {
        pairing.id: pairing for pairing in fetch_pairings_by_multiple_ids(alcohol_ids)
    }

    ranking_response = AlcoholRankingResponse()
    for idx, alcohol_id in enumerate(alcohol_ids):
        alcohol_response = PairingResponse.from_orm(alcohols_dict[alcohol_id])
        ranking_response.ranking.append(
            AlcoholRankResponse(
                rank=idx + 1,
                alcohol=alcohol_response,
            )
        )
    return ranking_response


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
