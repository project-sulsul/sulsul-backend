from typing import List
from pydantic import BaseModel

from core.domain.combination_model import Combination
from core.dto.pairing_dto import PairingResponse


class CombinationResponse(BaseModel):
    id: int
    alcohol: PairingResponse
    food: PairingResponse
    count: int
    description: str | None

    @classmethod
    def from_orm(cls, entity: Combination):
        print(entity)
        return CombinationResponse(
            id=entity.id,
            alcohol=PairingResponse.from_orm(entity.alcohol),
            food=PairingResponse.from_orm(entity.food),
            count=entity.count,
            description=entity.description,
        )
    

class CombinationListResponse(BaseModel):
    combinations: List[CombinationResponse]
