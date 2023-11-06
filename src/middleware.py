import typing
from functools import wraps
from ipaddress import IPv4Address, IPv4Network

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.datastructures import URL, Headers
from starlette.responses import PlainTextResponse, RedirectResponse, Response, JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send


ENFORCE_DOMAIN_WILDCARD = "Domain wildcard patterns must be like '*.example.com'."

class EnhancedTrustedHostMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        allowed_hosts: typing.Optional[typing.Sequence[str]] = None,
        allowed_cidrs: typing.Optional[typing.Sequence[str]] = None,
        www_redirect: bool = True,
    ) -> None:
        if allowed_hosts is None:
            allowed_hosts = ["*"]

        for pattern in allowed_hosts:
            assert "*" not in pattern[1:], ENFORCE_DOMAIN_WILDCARD
            if pattern.startswith("*") and pattern != "*":
                assert pattern.startswith("*."), ENFORCE_DOMAIN_WILDCARD
        
        self.app = app
        self.allowed_hosts = list(allowed_hosts)
        self.allowed_cidr_networks = [ IPv4Network(pattern) for pattern in allowed_cidrs ]
        self.allow_any = "*" in allowed_hosts
        self.www_redirect = www_redirect

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self.allow_any or scope["type"] not in ("http", "websocket",): # pragma: no cover
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        host = headers.get("host", "").split(":")[0]
        is_valid_host = False
        found_www_redirect = False
        for pattern in self.allowed_hosts:
            if host == pattern or (
                pattern.startswith("*") and host.endswith(pattern[1:])
            ):
                is_valid_host = True
                break
            elif "www." + host == pattern:
                found_www_redirect = True

        try:
            ipv4_host = IPv4Address(host)
            if not is_valid_host:
                for cidr_network in self.allowed_cidr_networks:
                    if ipv4_host in cidr_network:
                        is_valid_host = True
                        break
        except ValueError: 
            pass

        if is_valid_host:
            await self.app(scope, receive, send)
        else:
            response: Response
            if found_www_redirect and self.www_redirect:
                url = URL(scope=scope)
                redirect_url = url.replace(netloc="www." + url.netloc)
                response = RedirectResponse(url=str(redirect_url))
            else:
                response = PlainTextResponse("Invalid host header", status_code=400)
            await response(scope, receive, send)


def auth(call_next: RequestResponseEndpoint):
    """
    사용자 로그인 정보를 request.state.user에 바인딩 하기 위한 미들웨어
    
    -- Usage
        ```
        @router.get("/path")
        @auth
        async def some_handler_method(request: fastapi.Request):
            login_user = request.state.user
        ```
    
    - 해당 미들웨어 사용 시 핸들러 메소드는 request 매개변수를 필수로 받아야 함
    - 인증된 사용자의 경우 request.state.user: 디코드된 액세스 토큰 payload
    - 인증되지 않은 사용자의 경우 request.state.user: None
    """
    @wraps(call_next)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs["request"]
        # TODO get access token

        try:
            # TODO get login user
            pass

        except Exception as e:
            request.state.user = None

        return await call_next(*args, **kwargs)
    return wrapper
