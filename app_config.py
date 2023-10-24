from app import app

# from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi.staticfiles import StaticFiles

from src.middleware import EnhancedTrustedHostMiddleware


# Routers
from v1.router import v1_router
app.include_router(v1_router)


# Middlewares
app.add_middleware(
    EnhancedTrustedHostMiddleware, 
    allowed_hosts=[
        "localhost",
    ],
    allowed_cidrs=[

    ],
)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])


# Exception handlers
from src import exception_handler


# static path config
app.mount("/static", StaticFiles(directory="static"), name="static")


# favicon config
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("static/favicon.ico")
