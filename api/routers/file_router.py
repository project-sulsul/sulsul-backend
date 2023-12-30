from fastapi import UploadFile, APIRouter
from starlette.responses import JSONResponse

from core.util.file_util import upload_file_to_s3

router = APIRouter(
    prefix="/files",
    tags=["File (이미지 업로드)"],
)

directories = ["images"]


@router.post("/upload")
async def upload(file: UploadFile, directory: str):
    url = upload_file_to_s3(file, directory)
    return JSONResponse(content={"url": url})
