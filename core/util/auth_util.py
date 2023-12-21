from typing import Optional
from starlette.requests import Request


def get_login_user_id(request: Request) -> Optional[int]:
    token_info = request.state.token_info
    if token_info is not None:
        return token_info["id"]
    return None
