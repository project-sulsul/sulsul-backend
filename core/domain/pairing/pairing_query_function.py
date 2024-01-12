from typing import List

from core.domain.pairing.pairing_model import Pairing


def fetch_pairings_by_multiple_ids(pairing_ids: List[int]):
    query = (
        Pairing.select()
        .where(
            Pairing.id.in_(pairing_ids),
            Pairing.is_deleted == False,
        )
    )
    return query.execute()
