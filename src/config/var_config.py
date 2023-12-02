import os
from pytz import timezone


# 실행 환경이 운영인지 개발인지 확인
IS_PROD = (
    True
    if os.environ.get("PYTHONPATH") == "/var/app/venv/staging-LQM1lest/bin"
    else False
)


KST = timezone("Asia/Seoul")
ALG = "HS256"
ISSUER = ""  # TODO 도메인 연결 후 작성
TOKEN_TYPE = "Bearer"
TOKEN_DURATION = 60 * 60 * 24 * 7
ADMIN_TOKEN_DURATION = 60 * 60 * 12

JWT_COOKIE_OPTIONS = {
    "key": "access_token",
    "httponly": True,
    "secure": False,
    "samesite": "lax",
}

if os.environ.get("APPLE_CLIENT_ID"):
    APPLE_CLIENT_ID = os.environ.get("APPLE_CLIENT_ID")
else:
    from src.config.secrets import APPLE_CLIENT_ID

USER_NICKNAME_MAX_LENGTH = 10


# DB 프라이빗 서브넷으로 옮긴 후엔 아래 사용
# DB_HOST = os.environ.get("DB_HOST") if IS_PROD else "localhost"
# DB_PORT =os.environ.get("DB_PORT") if IS_PROD else 5432
# DB_USER = os.environ.get("DB_USER") if IS_PROD else "opponent"
# DB_PASSWORD = os.environ.get("DB_PASSWORD") if IS_PROD else "opponent"
# DB_NAME = "sulsul" if IS_PROD else "airflow"
# DB_SCHEMA = "sulsul" if IS_PROD else "test"

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = "sulsul"
DB_SCHEMA = "sulsul"


ADMIN_USER_UIDS = [
    "ahdwjdtprtm@gmail.com",
]
