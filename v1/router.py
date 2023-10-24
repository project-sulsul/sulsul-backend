from fastapi import APIRouter
from src.router_import_util import import_router_modules


v1_router = APIRouter(
    prefix="/v1",
    tags=["V1"]
)

import_router_modules(v1_router, "v1")
