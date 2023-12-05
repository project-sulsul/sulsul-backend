from pydantic import BaseModel

from core.config.var_config import TOKEN_TYPE, TOKEN_DURATION


class GoogleCredentialsModel(BaseModel):
    """
    구글 로그인/회원가입 모델
    - google_client_id (str): 구글 로그인 시 사용한 OAuth 2.0 클라이언트 ID
    - id_token (str): 구글 로그인 후 발급받은 ID TOKEN
    """

    google_client_id: str
    id_token: str


class KakaoCredentialsModel(BaseModel):
    """
    카카오 로그인/회원가입 모델
    - access_token (str): 카카오 로그인 후 발급받은 Access Token
    """

    access_token: str


class AppleCredentialsModel(BaseModel):
    """
    애플 로그인/회원가입 모델
    - id_token (str): 애플 로그인 후 발급받은 ID TOKEN
    """

    id_token: str


class TokenResponseModel(BaseModel):
    """
    로그인 성공 시 액세스 토큰 응답 모델
    - access_token (str): API 액세스 토큰
    - token_type (str): 토큰 인증 타입
    - expires_in (str): 토큰의 유효성 지속 시간(초)
    """

    user_id: int
    access_token: str
    token_type: str = TOKEN_TYPE
    expires_in: int = TOKEN_DURATION
