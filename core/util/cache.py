from typing import Optional, List

from core.config.orm_config import db
from core.domain.pairing.pairing_model import Pairing
from core.util.logger import logger


class PairingCacheStore:
    def __init__(self):
        self._pairing_cache = {}
        self.__set_all_pairing_cache()

    def __set_all_pairing_cache(self):
        db.connect()
        for pairing in Pairing.select().where(Pairing.is_deleted == False):
            self._pairing_cache[pairing.id] = pairing
        db.close()
        logger.info(f"load all pairing cache = {self._pairing_cache}")

    def get_all_names_by_ids(self, pairing_ids: List[int]) -> List[str]:
        return [self._pairing_cache[pairing_id].name for pairing_id in pairing_ids]

    def get_by_id(self, pairing_id: int) -> Optional[Pairing]:
        return self._pairing_cache[pairing_id]

    def get_all_by_type(self, pairing_type: str) -> List[Pairing]:
        return [
            pairing
            for pairing in self._pairing_cache.values()
            if pairing.type == pairing_type
        ]

    def get_all_by_names(self, pairing_names: List[str]) -> List[Pairing]:
        return [
            pairing
            for pairing in self._pairing_cache.values()
            if pairing.name in pairing_names
        ]


pairing_cache_store = PairingCacheStore()
