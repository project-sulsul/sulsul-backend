from fastapi import APIRouter, Depends, Request

from api.config.middleware import auth_required, auth
from api.descriptions.ranking_api_descriptions import GET_TAGS_RELATED_FEEDS_DESC
from core.config.orm_config import read_only
from core.config.var_config import DEFAULT_PAGE_SIZE
from core.domain import combination_query_function
from core.domain.feed_query_function import (
    fetch_related_feeds_by_tags,
)
from core.dto.combination_dto import CombinationResponse, CombinationListResponse
from core.dto.page_dto import CursorPageResponse
from core.util.auth_util import get_login_user_or_none
from core.util.feed_util import FeedResponseBuilder

router = APIRouter(
    prefix="/ranks",
    tags=["Ranking"],
)


@router.get(
    path="/combinations",
    dependencies=[Depends(read_only)],
    response_model=CombinationListResponse,
)
@auth_required
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
    dependencies=[Depends(read_only)],
    # response_model=
)
@auth_required
async def get_alcohol_ranking(request: Request):
    return


@router.get(
    path="/related-feeds",
    dependencies=[Depends(read_only)],
    response_model=CursorPageResponse,
    description=GET_TAGS_RELATED_FEEDS_DESC,
)
@auth
async def get_alcohol_related_feeds(
    request: Request,
    tags: str,  # comma separated tags
    next_feed_id: int = 0,
    size: int = DEFAULT_PAGE_SIZE,
):
    return FeedResponseBuilder.related_feeds(
        feeds=fetch_related_feeds_by_tags(tags.split(","), next_feed_id, size),
        size=size,
        login_user=get_login_user_or_none(request),
    )
