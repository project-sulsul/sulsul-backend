import os, jwt
from datetime import datetime, timedelta

from core.config.var_config import (
    IS_PROD,
    KST,
    ALG,
    ISSUER,
    TOKEN_DURATION,
    ADMIN_TOKEN_DURATION,
)

if IS_PROD:
    JWT_ENCRYPTION_KEY = os.environ.get("JWT_ENCRYPTION_KEY")
else:
    from core.config.secrets import JWT_ENCRYPTION_KEY


def build_token(**kwargs) -> str:
    current_time = datetime.now(KST)
    payload = {
        "iss": ISSUER,
        "iat": current_time,
        "exp": current_time + timedelta(seconds=TOKEN_DURATION),
    }
    payload.update(kwargs)

    return jwt.encode(
        payload=payload,
        key=JWT_ENCRYPTION_KEY,
        algorithm=ALG,
    )


def build_admin_token(**kwargs) -> str:
    current_time = datetime.now(KST)
    payload = {
        "iss": ISSUER,
        "iat": current_time,
        "exp": current_time + timedelta(seconds=ADMIN_TOKEN_DURATION),
    }
    payload.update(kwargs)

    return jwt.encode(
        payload=payload,
        key=JWT_ENCRYPTION_KEY,
        algorithm=ALG,
    )


def get_login_user(token: str) -> dict:
    return jwt.decode(
        jwt=token,
        key=JWT_ENCRYPTION_KEY,
        algorithms=ALG,
        verify=True,
        options={"verify_signature": True},
    )
