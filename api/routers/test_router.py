from typing import Optional

from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import JSONResponse
from fastapi_events.dispatcher import dispatch

from ai.inference import classify
from core.config.orm_config import transactional
from core.domain.user.user_model import User
from core.dto.auth_dto import TokenResponse
from core.event.events import CommentEvents, CreateCommentPayload
from core.util.file_util import upload_file_to_s3
from core.util.jwt import build_token

router = APIRouter(prefix="/test", tags=["테스트용 API"])


@router.get(
    "/jwt",
    dependencies=[Depends(transactional)],
    response_model=TokenResponse,
)
async def get_jwt_for_test(user_id: int):
    # if IS_PROD:
    #     raise ForbiddenException(
    #         "This API is only available in development environment"
    #     )

    user = User.get_by_id(user_id)

    token = build_token(
        id=user_id,
        social_type=user.social_type,
        status=user.status,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=TokenResponse(user_id=user.id, access_token=token).model_dump(),
    )


@router.post("/ai")
async def get_inference_from_image(image: UploadFile):
    url = upload_file_to_s3(image, "images")
    return classify(url)


@router.post("/error")
async def occur_unexpected_error(test_params: Optional[str] = None):
    raise Exception("Unexpected Error")


@router.post("/push")
async def send_push_notification():
    payload = CreateCommentPayload(
        comment_id=1,
        feed_owner_user_id=1,
        comment_writer_user_id=1,
    )
    dispatch(CommentEvents.CREATE_COMMENT, payload.model_dump())
