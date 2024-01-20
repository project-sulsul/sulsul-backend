import math
from datetime import datetime, timedelta
from typing import List

import pandas as pd

from core.client.naver_client import NaverApiClient
from core.config.orm_config import db
from core.domain.pairing.pairing_model import Pairing
from core.domain.ranking.search_volume_model import SearchVolume
from core.util.logger import logger


def fetch_keywords() -> List[str]:
    def flatten(lst):
        flat_list = [
            item
            for sublist in lst
            for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])
        ]
        return flat_list

    try:
        db.connect()
        keywords = [
            pairing.name.replace(" ", "").split("/")
            if "/" in pairing.name
            else pairing.name.replace(" ", "")
            for pairing in Pairing.select().where(Pairing.is_deleted == False)
        ]
        return flatten(keywords)
    finally:
        db.close()


def save_search_volume(name: str, volume: int, start_date: str, end_date: str):
    try:
        db.connect()
        SearchVolume.delete().where(
            SearchVolume.name == name,
            SearchVolume.start_date == start_date,
            SearchVolume.end_date == end_date,
        ).execute()
        SearchVolume.create(
            name=name, volume=volume, start_date=start_date, end_date=end_date
        )
        logger.info(f"[SearchVolume Batch] - {name} save success")
    except:
        db.rollback()
    finally:
        db.close()


start_date: str = ((datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d"),)
end_date: str = datetime.today().strftime("%Y-%m-%d")


def search_volume():
    naver_api_client = NaverApiClient()
    keywords = fetch_keywords()
    logger.info(f"[SearchVolume Batch] - keywords = {keywords}")
    for i in range(0, len(keywords), 5):
        # api 키워드는 최대 5개씩만 가능해서 5개씩 조회한다
        keywords_split_by_five = keywords[i : i + 5]
        logger.info(f"keywords_split_by_five = {keywords_split_by_five}")

        trend = naver_api_client.get_trends(keywords_split_by_five)
        volume = naver_api_client.get_volumes(keywords_split_by_five)

        for keyword in keywords_split_by_five:
            df = pd.DataFrame(trend[keyword]).set_index("period")
            df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
            df = df.reindex(
                index=pd.date_range(
                    start=df.index[0],
                    end=(datetime.today() - timedelta(1)).strftime("%Y-%m-%d"),
                ),
                fill_value=0.0,
            ).sort_index()
            ratio_sum = df["ratio"].tail(30).sum()
            coefficient = (volume[keyword] / ratio_sum) if ratio_sum != 0 else 0
            df["ratio"] = df["ratio"] * coefficient
            df = df.apply(lambda x: math.ceil(x.ratio), axis=1)
            df.index = df.index.strftime("%Y%m%d")

            logger.info(
                f"[SearchVolume Batch] - keyword = {keyword}, volume = {df.sum()}"
            )

            save_search_volume(keyword, df.sum(), start_date, end_date)


search_volume()
