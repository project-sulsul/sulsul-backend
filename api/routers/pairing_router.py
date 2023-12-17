from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse

from peewee import DoesNotExist

from api.descriptions.pairing_api_descriptions import REQUEST_PAIRING_BY_USER_DESC
from core.config.orm_config import transactional
from api.config.middleware import auth, auth_required

from core.domain.pairing_model import Pairing, PairingRequest
from core.dto.pairing_dto import (
    PairingSearchType,
    PairingRequestByUserRequest,
    PairingRequestByUserResponse,
)
from core.dto.pairing_dto import PairingResponse
from core.dto.pairing_dto import PairingListResponse

router = APIRouter(
    prefix="/pairings",
    tags=["Pairing (술, 안주)"],
)


@router.get(
    "", dependencies=[Depends(transactional)], response_model=PairingListResponse
)
@auth
async def get_pairings(request: Request, type: PairingSearchType):
    data = [
        PairingResponse.from_orm(pairing).model_dump()
        for pairing in Pairing.select().where(Pairing.is_deleted == False)
    ]
    if type is not PairingSearchType.전체:
        data = [pairing for pairing in data if pairing["type"] == type]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=PairingListResponse(pairings=data).model_dump(),
    )


@router.get(
    "/{pairing_id}",
    dependencies=[Depends(transactional)],
    response_model=PairingResponse,
)
@auth
async def get_pairing_by_id(request: Request, pairing_id: int):
    try:
        pairing = Pairing.get_by_id(pairing_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=PairingResponse.from_orm(pairing).model_dump(),
        )
    except DoesNotExist:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"Pairing {pairing_id} doesn't exist"},
        )


@router.post(
    "/requests",
    dependencies=[Depends(transactional)],
    response_model=PairingRequestByUserResponse,
    description=REQUEST_PAIRING_BY_USER_DESC,
)
@auth
async def save_pairing_request_by_user(
    request: Request, request_body: PairingRequestByUserRequest
):
    pairing_request = PairingRequest.create(**request_body.model_dump())
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=PairingRequestByUserResponse.from_orm(pairing_request).model_dump(),
    )
