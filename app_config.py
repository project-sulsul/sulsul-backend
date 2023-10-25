from app import app

import os
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi.staticfiles import StaticFiles
from peewee import PostgresqlDatabase

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


# Databases
db = PostgresqlDatabase(
    database=os.environ.get("DB_DBNAME") if os.environ.get("DB_DBNAME") else "airflow",
    host=os.environ.get("DB_HOST") if os.environ.get("DB_HOST") else "localhost",
    port=os.environ.get("DB_PORT") if os.environ.get("DB_PORT") else 5432,
    user=os.environ.get("DB_USER") if os.environ.get("DB_USER") else "opponent",
    password=os.environ.get("DB_PASSWORD") if os.environ.get("DB_HOST") else "opponent",
)
DB_SCHEMA = os.environ.get("DB_SCHEMA") if os.environ.get("DB_SCHEMA") else "test"

# DB init
import db_init


# Exception handlers
from src import exception_handler


# static path config
app.mount("/static", StaticFiles(directory="static"), name="static")


# favicon config
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("static/favicon.ico")
