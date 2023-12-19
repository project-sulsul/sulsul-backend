from fastapi import APIRouter, Depends, Request

from core.config.orm_config import get_db
from api.config.middleware import auth_required
from core.domain import combination_query_function
from core.dto.pairing_dto import PairingResponse
from core.dto.combination_dto import CombinationResponse, CombinationListResponse


router = APIRouter(
    prefix="/ranks",
    tags=["Ranking"],
)


@router.get(
    path="/combinations",
    dependencies=[Depends(get_db)],
    response_model=CombinationListResponse,
)
@auth_required
async def get_combination_ranking(request: Request, order_by_popular: bool = True):
    combinations = [CombinationResponse(**record) for record in combination_query_function.fetch_combination_ranking(order_by_popular)]
    return CombinationListResponse(combinations=combinations)


@router.get(
    path="/alcohol",
    dependencies=[Depends(get_db)],
    # response_model=
)
@auth_required
async def get_alcohol_ranking(request: Request):
    return