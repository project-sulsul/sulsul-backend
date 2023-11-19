import jwt
from datetime import datetime, timedelta

from src.config.secrets import JWT_ENCRYPTION_KEY
from src.config.var_config import *


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


def get_login_user(token: str) -> dict:
    return jwt.decode(
        jwt=token, 
        key=JWT_ENCRYPTION_KEY, 
        algorithms=ALG, 
        options={
            "verify_signature": True,
        }
    )