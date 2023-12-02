from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse

from peewee import DoesNotExist

from src.orm import transactional
from src.middleware import auth, auth_required
from v1.pairing.model import Pairing, PairingSearchType
from v1.pairing.model import PairingResponseModel
from v1.pairing.model import PairingListResponseModel


router = APIRouter(
    prefix="/pairings",
    tags=["Pairing"],
)


@router.get(
    "", dependencies=[Depends(transactional)], response_model=PairingListResponseModel
)
@auth
async def get_pairings(request: Request, type: PairingSearchType):
    data = [
        pairing.dto().model_dump()
        for pairing in Pairing.select().where(Pairing.is_deleted == False)
    ]
    if type is not PairingSearchType.전체:
        data = [pairing for pairing in data if pairing["type"] == type]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=PairingListResponseModel(pairings=data).model_dump(),
    )


@router.get(
    "/{pairing_id}",
    dependencies=[Depends(transactional)],
    response_model=PairingResponseModel,
)
@auth
async def get_pairing_by_id(request: Request, pairing_id: int):
    try:
        pairing = Pairing.get_by_id(pairing_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=pairing.dto().model_dump()
        )
    except DoesNotExist:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"Pairing {pairing_id} doesn't exist"},
        )
