import os
import importlib

from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi import Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app import app
from api.config.middleware import EnhancedTrustedHostMiddleware


# Routers
from admin.router import router as admim_router
app.include_router(admim_router)

for filename in os.listdir("api/routers"):
    if "_router.py" not in filename: continue
    if filename == "file_router.py": continue
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


@app.on_event("startup")
def on_startup():
    import core.db_init_tables


@app.get("/")
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
