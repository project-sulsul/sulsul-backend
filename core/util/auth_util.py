from typing import Optional
from starlette.requests import Request

from core.domain.user_model import User


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
