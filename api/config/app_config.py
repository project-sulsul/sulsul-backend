import importlib
import logging
import os
from asyncio import create_task
from datetime import datetime

from fastapi import Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.types import Message
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

# Routers
from admin.router import router as admim_router
from api.config.middleware import EnhancedTrustedHostMiddleware
from app import app
from core.util.slack import send_slack_message

# from core.event.push_event_handler import handle_create_comment_send_push_handler

app.include_router(admim_router)

for filename in os.listdir("api/routers"):
    if "_router.py" not in filename:
        continue
    # if filename == "test_router.py" and IS_PROD:
    #     continue

    module = importlib.import_module("api.routers." + filename.split(".")[0])
    if hasattr(module, "router"):
        app.include_router(module.router)

# Middlewares
app.add_middleware(
    EnhancedTrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "sulsul-env-1.eba-7i2eztxj.ap-northeast-2.elasticbeanstalk.com",
        "sulsul.link",
    ],
    allowed_cidrs=[
        "10.0.0.0/16",  # VPC
    ],
)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])
app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])

origins = [
    # "http://localhost",
    # "http://localhost:3000",
    # "https://sul-sul-admin.vercel.app/",
    # "https://sul-sul-admin.vercel.app".
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


logging_paths = [
    "/admin",
    "/auth",
    "/feeds",
    "/pairings",
    "/ranks",
    "/reports",
    "/users",
]


@app.middleware("http")
async def request_response_logging_middleware(request: Request, call_next):
    if not request.url.path.startswith(tuple(logging_paths)):
        return await call_next(request)

    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)

    res_body = b""
    async for chunk in response.body_iterator:
        res_body += chunk

    message = f"""
    ##################################################################
    [{datetime.now()}] status_code: {response.status_code}
    {request.method} {str(request.url)}
    request : {req_body.decode()}
    response : {res_body.decode()}
    """

    if str(response.status_code).startswith("4"):
        channel = "#error-logs"
    else:
        channel = "#api-logs"

    create_task(
        send_slack_message(
            channel=channel,
            icon_emoji=":collision:",
            sender_name="API 요청 알리미",
            message=message,
        )
    )
    return Response(
        status_code=response.status_code,
        headers=response.headers,
        content=res_body.decode(),
        media_type=response.media_type,
    )


@app.on_event("startup")
def on_startup():
    from core.config.var_config import IS_PROD

    if not IS_PROD:
        logger = logging.getLogger("peewee")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)


@app.get("/", include_in_schema=False)
async def redirect_to_docs(request: Request):
    return RedirectResponse("/docs")


# Exception handlers

# static path config
app.mount("/static", StaticFiles(directory="admin/static"), name="static")


# favicon config
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("admin/static/favicon.png")
