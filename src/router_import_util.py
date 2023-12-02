import os
import importlib
from fastapi import APIRouter


def import_router_modules(
    router: APIRouter,
    version: str,
    except_dirs: list[str] = [],
):
    for dirname in os.listdir(version):
        if dirname in except_dirs:
            continue

        if len(dirname.split(".")) == 1 and dirname != "__pycache__":
            file_list = os.listdir(f"{version}/{dirname}")
            if "router.py" in file_list:
                module = importlib.import_module(f"{version}.{dirname}.router")

                if hasattr(module, "router"):
                    router.include_router(module.router)
