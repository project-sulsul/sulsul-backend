from typing import Optional

from fastapi.security import HTTPBearer
from starlette.requests import Request

from api.config.exceptions import UnauthorizedException
from core.domain.user.user_model import User
from core.util.jwt import decode_token


def get_login_user_id(request: Request) -> int:
    """
    -1은 User.get_or_noe()에서 None을 반환하기 위함
    None을 반환하면 User.get_or_none()에서 첫번째 record를 반환함
    """
    token_info = request.state.token_info
    if token_info is not None:
        return token_info["id"]
    return -1


def get_login_user_or_none(request: Request) -> Optional[User]:
    return User.get_or_none(get_login_user_id(request))


class AuthRequired(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthRequired, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise UnauthorizedException("Unauthorized user cannot access")

        token_type, token = auth_header.split(" ")

        if token_type != "Bearer":
            raise UnauthorizedException("Invalid token type")

        try:
            request.state.token_info = decode_token(token)
        except Exception as e:
            raise UnauthorizedException("Invalid token")


class AuthOptional(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthOptional, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        try:
            auth_header = request.headers.get("Authorization")
            token_type, token = auth_header.split(" ")
            request.state.token_info = decode_token(token)
        except Exception as e:
            request.state.token_info = None
            pass
