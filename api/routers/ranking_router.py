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
from core.domain.ranking.ranking_model import Ranking
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
    ranking: Ranking = [
        ranking for ranking in Ranking.select().order_by(Ranking.id.desc()).limit(1)
    ][0]
    response = CombinationRankingResponse(
        start_date=ranking.start_date.strftime("%Y-%m-%d"),
        end_date=ranking.end_date.strftime("%Y-%m-%d"),
    )
    for rank, combination in ranking.ranking["combination"].items():
        rank_dto = CombinationRankResponse(
            rank=rank,
            pairings=[PairingResponse(**comb) for comb in combination],
        )
        response.ranking.append(rank_dto)
    return response


@router.get(
    path="/alcohol",
    dependencies=[Depends(read_only), Depends(AuthOptional())],
    response_model=AlcoholRankingResponse,
    description=GET_ALCOHOL_RANKING_DESC,
)
async def get_alcohol_ranking(request: Request):
    ranking: Ranking = [
        ranking for ranking in Ranking.select().order_by(Ranking.id.desc()).limit(1)
    ][0]
    response = AlcoholRankingResponse(
        start_date=ranking.start_date.strftime("%Y-%m-%d"),
        end_date=ranking.end_date.strftime("%Y-%m-%d"),
    )
    for rank, alcohol in ranking.ranking["alcohol"].items():
        response.ranking.append(
            AlcoholRankResponse(
                rank=rank,
                alcohol=PairingResponse(**alcohol),
                description=None,
            )
        )
    return response


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
