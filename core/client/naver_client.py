import hashlib
import hmac
import os
import time
from base64 import b64encode
from datetime import datetime, timedelta
from typing import List

import requests

try:
    from core.config.secrets import (
        NAVER_TREND_API_CLIENT_ID,
        NAVER_TREND_API_CLIENT_SECRET,
        NAVER_VOLUME_API_CUSTOMER_ID,
        NAVER_VOLUME_API_ACCESS_LICENCE,
        NAVER_VOLUME_API_PRIVATE_KEY,
    )

    NAVER_TREND_API_CLIENT_ID = NAVER_TREND_API_CLIENT_ID
    NAVER_TREND_API_CLIENT_SECRET = NAVER_TREND_API_CLIENT_SECRET
    NAVER_VOLUME_API_CUSTOMER_ID = NAVER_VOLUME_API_CUSTOMER_ID
    NAVER_VOLUME_API_ACCESS_LICENCE = NAVER_VOLUME_API_ACCESS_LICENCE
    NAVER_VOLUME_API_PRIVATE_KEY = NAVER_VOLUME_API_PRIVATE_KEY
except Exception:
    NAVER_TREND_API_CLIENT_ID = os.getenv("NAVER_TREND_API_CLIENT_ID")
    NAVER_TREND_API_CLIENT_SECRET = os.getenv("NAVER_TREND_API_CLIENT_SECRET")
    NAVER_VOLUME_API_CUSTOMER_ID = os.getenv("NAVER_VOLUME_API_CUSTOMER_ID")
    NAVER_VOLUME_API_ACCESS_LICENCE = os.getenv("NAVER_VOLUME_API_ACCESS_LICENCE")
    NAVER_VOLUME_API_PRIVATE_KEY = os.getenv("NAVER_VOLUME_API_PRIVATE_KEY")


class NaverApiClient:
    def __generate_signature(self):
        timestamp = str(round(time.time() * 1000))
        hash = hmac.new(
            key=bytes(NAVER_VOLUME_API_PRIVATE_KEY, "utf-8"),
            msg=bytes(f"{timestamp}.GET./keywordstool", "utf-8"),
            digestmod=hashlib.sha256,
        )
        hash.hexdigest()
        return timestamp, b64encode(hash.digest())

    def get_trends(
        self,
        keywords: List[str],
        start_date: str = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d"),
        end_date: str = datetime.today().strftime("%Y-%m-%d"),
        time_unit: str = "date",
    ):
        form = {
            "url": "https://openapi.naver.com/v1/datalab/search",
            "headers": {
                "X-Naver-Client-Id": NAVER_TREND_API_CLIENT_ID,
                "X-Naver-Client-Secret": NAVER_TREND_API_CLIENT_SECRET,
            },
            "json": {
                "startDate": start_date,
                "endDate": end_date,
                "timeUnit": time_unit,
                "keywordGroups": [
                    {"groupName": keyword, "keywords": [keyword]}
                    for keyword in keywords
                ],
            },
        }

        response = requests.post(**form)
        if response.status_code == 200:
            results = response.json()["results"]
            data = dict()
            for result in results:
                data[result["title"]] = result["data"]
            return data
        else:
            raise Exception(response.content)

    def get_volumes(self, keywords: List[str]):
        timestamp, signature = self.__generate_signature()
        form = {
            "url": "https://api.naver.com/keywordstool",
            "headers": {
                "X-Customer": NAVER_VOLUME_API_CUSTOMER_ID,
                "X-Api-Key": NAVER_VOLUME_API_ACCESS_LICENCE,
                "X-Timestamp": timestamp,  # 요청하는 타임스탬프를 찍어서 보내야함
                "X-Signature": signature,  # 시그니처를 만들어서 요청을 보내야함
            },
            "params": {"hintKeywords": ",".join(keywords), "event": "1", "month": "1"},
        }

        response = requests.get(**form)
        if response.status_code == 200:
            keyword_list = response.json()["keywordList"]
            data = dict()
            for item in keyword_list:
                if len(data) == len(keywords):
                    break
                if item["relKeyword"] in keywords:
                    if isinstance(item["monthlyPcQcCnt"], str):
                        item["monthlyPcQcCnt"] = 0
                    if isinstance(item["monthlyMobileQcCnt"], str):
                        item["monthlyMobileQcCnt"] = 0
                    data[item["relKeyword"]] = (
                        item["monthlyPcQcCnt"] + item["monthlyMobileQcCnt"]
                    )
            return data
        else:
            raise Exception(response.content)
