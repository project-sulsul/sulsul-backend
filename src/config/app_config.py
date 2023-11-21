from app import app

import os
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.middleware import EnhancedTrustedHostMiddleware


# Routers
from admin.router import router as admim_router
app.include_router(admim_router)

from v1.root_router import v1_root_router
app.include_router(v1_root_router)


# Middlewares
app.add_middleware(
    EnhancedTrustedHostMiddleware, 
    allowed_hosts=[
        "localhost",
        "sulsul-env.eba-gvmvk4bq.ap-northeast-2.elasticbeanstalk.com",
    ],
    allowed_cidrs=[

    ],
)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])


@app.on_event("startup")
def on_startup():
    import src.db_init_tables

@app.get("/")
async def redirect_to_docs(request: Request):
    return RedirectResponse("/docs")


# Exception handlers
from src import exception_handler


# static path config
app.mount("/static", StaticFiles(directory="static"), name="static")


# favicon config
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("static/favicon.ico")
