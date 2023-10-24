import os
from datetime import timezone, timedelta


# Timezone config
KST = timezone(timedelta(hours=9))
ALG = ""
ISSUER = ""
TOKEN_DURATION = 60 * 60 * 24

JWT_COOKIE_OPTIONS = {
    "key": "access_token",
    "max_age": TOKEN_DURATION,
    "httponly": True,
    "secure": True,
    "samesite": "lax",
}

# Database config
DB_HOST = os.environ.get("DB_HOST") if os.environ.get("DB_HOST") else "localhost"
DB_PORT = os.environ.get("DB_PORT") if os.environ.get("DB_PORT") else 5432
DB_DBNAME = os.environ.get("DB_DBNAME") if os.environ.get("DB_DBNAME") else "airflow"
DB_USER = os.environ.get("DB_USER") if os.environ.get("DB_USER") else "opponent"
DB_PASSWORD = os.environ.get("DB_PASSWORD") if os.environ.get("DB_HOST") else "opponent"
DB_SCHEMA = os.environ.get("DB_SCHEMA") if os.environ.get("DB_SCHEMA") else "test"
