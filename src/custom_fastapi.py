from fastapi import FastAPI, APIRouter


class CustomFastAPI(FastAPI):

    def include_routers_with_version(self, api_routers: list[APIRouter], version: str):
        for api_router in api_routers:
            self.router.include_router(api_router, prefix=f"/v{version}")

