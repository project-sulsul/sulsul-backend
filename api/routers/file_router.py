from enum import Enum

from fastapi import UploadFile, APIRouter, Depends
from starlette.responses import JSONResponse

from api.descriptions.file_api_descriptions import UPLOAD_FILE_DESC
from core.util.auth_util import AuthRequired
from core.util.file_util import upload_file_to_s3

router = APIRouter(
    prefix="/files",
    tags=["File (이미지 업로드)"],
)


class FileDirectory(Enum):
    IMAGES = "images"


@router.post(
    "/upload", dependencies=[Depends(AuthRequired())], description=UPLOAD_FILE_DESC
)
async def upload(file: UploadFile, directory: FileDirectory):
    url = upload_file_to_s3(file, directory.value)
    return JSONResponse(content={"url": url})
