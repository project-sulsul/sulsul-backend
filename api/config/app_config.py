import os
import importlib

from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from starlette.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi import Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app import app
from api.config.middleware import EnhancedTrustedHostMiddleware

import logging

# Routers
from admin.router import router as admim_router

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
        "sulsul-env.eba-gvmvk4bq.ap-northeast-2.elasticbeanstalk.com",
    ],
    allowed_cidrs=[],
)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])
app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    import core.db_init_tables
    from core.config.var_config import IS_PROD

    if not IS_PROD:
        logger = logging.getLogger("peewee")
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)


@app.get("/", include_in_schema=False)
async def redirect_to_docs(request: Request):
    return RedirectResponse("/docs")


# Exception handlers
from api.config import exception_handler

# static path config
app.mount("/static", StaticFiles(directory="admin/static"), name="static")


# favicon config
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("admin/static/favicon.png")
