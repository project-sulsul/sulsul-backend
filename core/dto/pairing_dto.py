from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel

from core.domain.pairing_model import Pairing


class PairingCreateRequest(BaseModel):
    type: str
    name: str
    image: str | None
    description: str | None


class PairingUpdateRequest(BaseModel):
    type: str
    name: str
    image: str | None
    description: str | None
    is_deleted: bool


class PairingResponse(BaseModel):
    id: int
    type: str
    name: str
    image: str | None
    description: str | None

    @classmethod
    def from_orm(cls, entity: Pairing):
        return PairingResponse(
            id=entity.id,
            type=entity.type,
            name=entity.name,
            image=entity.image,
            description=entity.description,
        )


class PairingAdminResponse(BaseModel):
    id: int
    type: str
    name: str
    image: str | None
    description: str | None
    created_at: str
    updated_at: str
    is_deleted: bool

    @classmethod
    def from_orm(cls, entity: Pairing):
        return PairingAdminResponse(
            id=entity.id,
            type=entity.type,
            name=entity.name,
            image=entity.image,
            description=entity.description,
            created_at=entity.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            updated_at=entity.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
            is_deleted=entity.is_deleted,
        )


class PairingListResponse(BaseModel):
    pairings: List[PairingResponse]


class PairingSearchType(str, Enum):
    전체 = "전체"
    술 = "술"
    안주 = "안주"
