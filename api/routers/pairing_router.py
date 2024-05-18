from fastapi import APIRouter, Depends

from api.descriptions.pairing_api_descriptions import REQUEST_PAIRING_BY_USER_DESC
from core.config.orm_config import transactional, read_only
from core.domain.pairing.pairing_model import Pairing
from core.domain.pairing.pairing_request_model import PairingRequest
from core.dto.pairing_dto import PairingListResponse
from core.dto.pairing_dto import PairingResponse
from core.dto.pairing_dto import (
    PairingSearchType,
    PairingRequestByUserRequest,
    PairingRequestByUserResponse,
)

router = APIRouter(
    prefix="/pairings",
    tags=["Pairing (술, 안주)"],
)


@router.get("", dependencies=[Depends(read_only)], response_model=PairingListResponse)
async def get_pairings(type: PairingSearchType):
    if type is not PairingSearchType.전체:
        pairings = (
            Pairing.select()
            .where(Pairing.is_deleted == False, Pairing.type == type)
            .order_by(Pairing.order)
        )
    else:
        pairings = Pairing.select().where(Pairing.is_deleted == False)

    response = [PairingResponse.from_orm(pairing) for pairing in pairings]

    return PairingListResponse(pairings=response)


@router.get(
    "/{pairing_id}",
    dependencies=[Depends(read_only)],
    response_model=PairingResponse,
)
async def get_pairing_by_id(pairing_id: int):
    pairing = Pairing.get_or_raise(pairing_id)
    return PairingResponse.from_orm(pairing)


@router.post(
    "/requests",
    dependencies=[Depends(transactional)],
    response_model=PairingRequestByUserResponse,
    description=REQUEST_PAIRING_BY_USER_DESC,
)
async def save_pairing_request_by_user(request_body: PairingRequestByUserRequest):
    found_pairing_requests = list(
        PairingRequest.select()
        .where(
            PairingRequest.subtype == request_body.subtype,
            PairingRequest.name == request_body.name,
            PairingRequest.is_deleted == False,
        )
        .execute()
    )

    if found_pairing_requests:
        pairing_request = found_pairing_requests[0]
        pairing_request.requested_count += 1
        pairing_request.save()
    else:
        pairing_request = PairingRequest.create(**request_body.model_dump())

    return PairingRequestByUserResponse.from_orm(pairing_request)
