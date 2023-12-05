from fastapi import HTTPException
import requests


class NicknameGeneratorClient:
    
    @classmethod
    def generate_random_nickname(cls, count: int = 30):
        response = requests.get(
            url="https://nickname.hwanmoo.kr",
            params={"format": "json", "count": count}
        )
        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)
        
        return response.json()["words"]
