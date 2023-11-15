import os
from pytz import timezone


# 실행 환경이 운영인지 개발인지 확인
IS_PROD = True if os.environ.get("PYTHONPATH") == "/var/app/venv/staging-LQM1lest/bin" else False


KST = timezone("Asia/Seoul")
ALG = "HS256"
ISSUER = "" # TODO 도메인 연결 후 작성
TOKEN_DURATION = 60 * 60 * 24

JWT_COOKIE_OPTIONS = {
    "key": "access_token",
    "max_age": TOKEN_DURATION,
    "httponly": True,
    "secure": True,
    "samesite": "lax",
}


DB_NAME = os.environ.get("DB_DBNAME") if os.environ.get("DB_DBNAME") else "airflow"
DB_HOST = os.environ.get("DB_HOST") if os.environ.get("DB_HOST") else "localhost"
DB_PORT =os.environ.get("DB_PORT") if os.environ.get("DB_PORT") else 5432
DB_USER = os.environ.get("DB_USER") if os.environ.get("DB_USER") else "opponent"
DB_PASSWORD = os.environ.get("DB_PASSWORD") if os.environ.get("DB_HOST") else "opponent"
DB_SCHEMA = os.environ.get("DB_SCHEMA") if os.environ.get("DB_SCHEMA") else "test"
