import os
import urllib
import uuid

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from fastapi import UploadFile, APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from api.config.middleware import auth_required
from core.config.var_config import IS_PROD

if IS_PROD:
    s3 = boto3.client(
        service_name="s3",
        aws_access_key_id=os.environ.get("AWS_S3_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_S3_SECRET_ACCESS_KEY"),
    )
else:
    from core.config import secrets

    s3 = boto3.client(
        service_name="s3",
        aws_access_key_id=secrets.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=secrets.AWS_S3_PRIVATE_KEY,
    )

BUCKET_NAME = "sulsul-s3"

router = APIRouter(
    prefix="/files",
    tags=["File (이미지 업로드)"],
)

directories = ["images"]


@router.post("/upload")
async def upload(file: UploadFile, directory: str):
    if directory not in directories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid directory"
        )

    filename = f"{str(uuid.uuid4())}.jpg"
    s3_key = f"{directory}/{filename}"

    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, s3_key)
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"S3 upload failed: {str(e)}",
        )

    url = "https://s3-ap-northeast-2.amazonaws.com/%s/%s" % (
        BUCKET_NAME,
        urllib.parse.quote(s3_key, safe="~()*!.'"),
    )
    return JSONResponse(content={"url": url})