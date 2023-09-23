from app import app

from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi.staticfiles import StaticFiles


# Routers
from auth.router import auth_router
app.include_router(auth_router)


# Middlewares
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])


# static path config
app.mount("/static", StaticFiles(directory="static"), name="static")


# favicon config
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("static/favicon.ico")
