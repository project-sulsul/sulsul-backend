from fastapi import FastAPI

app = FastAPI()

from app_config import *


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="app:app",
        port=8000,
        reload=True,
    )
