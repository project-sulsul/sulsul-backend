from typing import List, Optional
from pydantic import BaseModel

from core.dto.pairing_dto import PairingResponse


class CombinationRankResponse(BaseModel):
    rank: int = 1
    pairings: List[PairingResponse] = []
    description: Optional[str] = None


class CombinationRankingResponse(BaseModel):
    ranking: List[CombinationRankResponse] = []
