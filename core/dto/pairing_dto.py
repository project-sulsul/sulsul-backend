from enum import Enum
from typing import List, Optional

from core.domain.pairing_model import Pairing
from core.dto.base_dto import BaseDTO


class PairingCreateRequest(BaseDTO):
    type: str
    name: str
    image: Optional[str]
    description: Optional[str]


class PairingUpdateRequest(BaseDTO):
    type: str
    name: str
    subtype: str
    image: Optional[str]
    description: Optional[str]
    is_deleted: bool


class PairingResponse(BaseDTO):
    id: int
    type: str
    subtype: str
    name: str
    image: Optional[str]
    description: Optional[str]


class PairingAdminResponse(BaseDTO):
    id: int
    type: str
    subtype: str
    name: str
    image: Optional[str]
    description: Optional[str]
    created_at: str
    updated_at: str
    is_deleted: bool

    @classmethod
    def from_orm(cls, entity: Pairing):
        return PairingAdminResponse(
            id=entity.id,
            type=entity.type,
            subtype=entity.subtype,
            name=entity.name,
            image=entity.image,
            description=entity.description,
            created_at=entity.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            updated_at=entity.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
            is_deleted=entity.is_deleted,
        )


class PairingListResponse(BaseDTO):
    pairings: List[PairingResponse]


class PairingSearchType(str, Enum):
    전체 = "전체"
    술 = "술"
    안주 = "안주"


class PairingRequestByUserRequest(BaseDTO):
    type: str
    subtype: str
    name: str


class PairingRequestByUserResponse(BaseDTO):
    id: int
    type: str
    subtype: str
    name: str
