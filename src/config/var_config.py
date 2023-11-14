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
