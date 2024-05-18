print("============================================================================")
try:
    import sys

    sys.path.append(".")
    sys.path.append("/lambda")

    # DEBUG
    import os

    print(os.getenv("IS_PROD"))
    from core.config.var_config import IS_PROD, KST

    print(IS_PROD)

    from datetime import datetime, timedelta

    from core.config.orm_config import db
    from core.domain.ranking.ranking_model import Ranking
    from core.dto.pairing_dto import PairingResponse
    from core.domain.pairing.pairing_query_function import (
        fetch_pairings_by_multiple_ids,
    )
    from core.domain.ranking.ranking_query_function import (
        fetch_like_counts_group_by_alcohol,
        fetch_like_counts_group_by_combination,
    )

    def lambda_handler(event, context):
        today = datetime.now(KST).replace(hour=0, minute=0, second=0, microsecond=0)
        start = today - timedelta(days=today.weekday() + 3)
        end = start + timedelta(days=7)
        print(start)
        print(end)

        db.connect()

        # 술 랭킹
        alcohol_ids = []
        query = fetch_like_counts_group_by_alcohol(
            start_date=start,
            end_date=end,
            execute=False,
        )
        for row in query.execute():
            alcohol_ids.append(row.alcohol_id)

        alcohols_dict = {
            pairing.id: pairing
            for pairing in fetch_pairings_by_multiple_ids(alcohol_ids)
        }

        alcohol_ranking = {}
        for idx, alcohol_id in enumerate(alcohol_ids):
            rank = idx + 1
            alcohol_response = PairingResponse.from_orm(
                alcohols_dict[alcohol_id]
            ).__dict__
            alcohol_ranking[rank] = alcohol_response

        # 조합 랭킹
        data = []
        pairing_ids = set()
        query = fetch_like_counts_group_by_combination(
            start_date=start,
            end_date=end,
            execute=False,
        )
        for row in query.execute():
            data.append(row.combined_ids)
            pairing_ids.update(row.combined_ids)

        pairings_dict = {
            pairing.id: pairing
            for pairing in fetch_pairings_by_multiple_ids(pairing_ids=pairing_ids)
        }

        combination_ranking = {}
        for idx, pairing_ids in enumerate(data):
            rank = idx + 1
            combination_ranking[rank] = []
            for pairing_id in pairing_ids:
                combination_ranking[rank].append(
                    PairingResponse.from_orm(pairings_dict[pairing_id]).__dict__
                )

        import json

        print("술 랭킹: ")
        print(json.dumps(alcohol_ranking, ensure_ascii=False, indent=4))
        print("조합 랭킹: ")
        print(json.dumps(combination_ranking, ensure_ascii=False, indent=4))

        Ranking(
            start_date=start,
            end_date=end,
            ranking={
                "alcohol": alcohol_ranking,
                "combination": combination_ranking,
            },
        ).save()

        db.close()

except:
    import traceback

    print(traceback.format_exc())
