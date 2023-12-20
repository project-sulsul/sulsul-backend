from starlette.requests import Request


def get_login_user_id(request: Request) -> int | None:
    token_info = request.state.token_info
    if token_info is not None:
        return token_info["id"]
    return None
