from typing import Dict
from pydantic import BaseModel


class GoogleCredentialsModel(BaseModel):
    """
    구글 로그인/회원가입 양식  
    nickname, preference는 회원가입 시에만 작성  
    
    - google_client_id (str): 구글 로그인 시 사용한 OAuth 2.0 클라이언트 ID  
    - id_token (str): 구글 로그인 후 발급받은 ID TOKEN  
    """
    google_client_id: str
    id_token: str


class KakaoCredentialsModel(BaseModel):
    access_token: str
