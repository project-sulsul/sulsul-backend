from typing import List, Optional
from pydantic import BaseModel

from core.dto.pairing_dto import PairingResponse


class CombinationRankResponse(BaseModel):
    rank: int = 1
    pairings: List[PairingResponse] = []
    description: Optional[str] = None


# TODO : start_date, end_date 필드 추가
class CombinationRankingResponse(BaseModel):
    start_date: str = "12/01"
    end_date: str = "12/07"
    ranking: List[CombinationRankResponse] = []


class AlcoholRankResponse(BaseModel):
    rank: int = 1
    alcohol: PairingResponse
    description: Optional[str] = None


class AlcoholRankingResponse(BaseModel):
    start_date: str = "12/01"
    end_date: str = "12/07"
    ranking: List[AlcoholRankResponse] = []
