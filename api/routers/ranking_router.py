from fastapi import APIRouter, Depends, Request

from core.config.orm_config import get_db
from api.config.middleware import auth_required
from core.domain.combination_query_function import fetch_combination_ranking
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
    combinations = []
    for record in fetch_combination_ranking(order_by_popular):
        (
            id,
            count,
            description,
            alcohol_id,
            alcohol_type,
            alcohol_subtype,
            alcohol_name,
            alcohol_image,
            alcohol_description,
            food_id,
            food_type,
            food_subtype,
            food_name,
            food_image,
            food_description,
        ) = record
        combinations.append(
            CombinationResponse(
                id=id,
                alcohol=PairingResponse(
                    id=alcohol_id,
                    type=alcohol_type,
                    subtype=alcohol_subtype,
                    name=alcohol_name,
                    image=alcohol_image,
                    description=alcohol_description,
                ),
                food=PairingResponse(
                    id=food_id,
                    type=food_type,
                    subtype=food_subtype,
                    name=food_name,
                    image=food_image,
                    description=food_description,
                ),
                count=count,
                description=description,
            )
        )
    return CombinationListResponse(combinations=combinations)


@router.get(
    path="/alcohol",
    dependencies=[Depends(get_db)],
    # response_model=
)
@auth_required
def get_alcohol_ranking(request: Request):
    return
