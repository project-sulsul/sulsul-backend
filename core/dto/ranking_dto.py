from typing import List, Optional
from pydantic import BaseModel

from core.dto.pairing_dto import PairingResponse
from core.util.time import get_start_of_week_and_end_of_week


class CombinationRankResponse(BaseModel):
    rank: int = 1
    pairings: List[PairingResponse] = []
    description: Optional[str] = None


class CombinationRankingResponse(BaseModel):
    start_date: str = get_start_of_week_and_end_of_week()[0].strftime("%m/%d")
    end_date: str = get_start_of_week_and_end_of_week()[1].strftime("%m/%d")
    ranking: List[CombinationRankResponse] = []


class AlcoholRankResponse(BaseModel):
    rank: int = 1
    alcohol: PairingResponse
    description: Optional[str] = None


class AlcoholRankingResponse(BaseModel):
    start_date: str = "12/01"
    end_date: str = "12/07"
    ranking: List[AlcoholRankResponse] = []
