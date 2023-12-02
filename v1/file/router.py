import urllib
import uuid

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from fastapi import UploadFile, APIRouter, HTTPException
from starlette.responses import JSONResponse

from src.config.secrets import AWS_S3_ACCESS_KEY, AWS_S3_PRIVATE_KEY

s3 = boto3.client(
    "s3", aws_access_key_id=AWS_S3_ACCESS_KEY, aws_secret_access_key=AWS_S3_PRIVATE_KEY
)

BUCKET_NAME = "sulsul-s3"

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)

directories = ["images"]


@router.post("/upload")
async def upload(file: UploadFile, directory: str):
    if directory not in directories:
        raise HTTPException(status_code=400, detail="유효하지 않는 디렉토리에요")

    filename = f"{str(uuid.uuid4())}.jpg"
    s3_key = f"{directory}/{filename}"

    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, s3_key)
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"S3 upload fails: {str(e)}")

    url = "https://s3-ap-northeast-2.amazonaws.com/%s/%s" % (
        BUCKET_NAME,
        urllib.parse.quote(s3_key, safe="~()*!.'"),
    )
    return JSONResponse(content={"url": url})
