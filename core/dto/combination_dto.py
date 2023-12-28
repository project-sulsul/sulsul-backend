from typing import List, Optional
from pydantic import BaseModel

from core.domain.combination.combination_model import Combination
from core.dto.pairing_dto import PairingResponse


class CombinationResponse(BaseModel):
    id: int
    alcohol: PairingResponse
    food: PairingResponse
    count: int
    description: Optional[str]

    # @classmethod
    # def from_orm(cls, entity: Combination):
    #     dto = super().from_orm(entity)
    #     dto.alcohol = PairingResponse.from_orm(entity.alchohol)
    #     dto.food = PairingResponse.from_orm(entity.food)
    #     return dto

    @classmethod
    def from_orm(cls, entity: Combination):
        return CombinationResponse(
            **entity.__data__,
            alcohol=PairingResponse.from_orm(entity.alcohol),
            food=PairingResponse.from_orm(entity.food),
        )


class CombinationListResponse(BaseModel):
    combinations: List[CombinationResponse]
