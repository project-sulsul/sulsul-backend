from enum import Enum
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


class AiModel(Enum):
    RESNET_18 = "resnet18"
    RESNET_34 = "resnet34"
    RESNET_50 = "resnet50"


@router.post(
    "/ai",
    description="""
AI 모델 성능 테스트용 API (측정 완료되면 삭제 예정)
모델을 바꿔가면서 성능 측정 부탁드립니다! 최대한 직접 찍은 사진이면 좋아요 ㅎㅎ 현재로써는 34모델이 성능이 젤 좋습니다.

- threshold : 0.5 디폴트로 이 값을 변경함으로써 성능을 또 다르게 측정할 수 있어요. 요 값도 요리조리 변경해보시면서 측정 해주시면 감사드립니다! (0~1 사이값)
- 이미지가 실제로 클라우드에 올라가서, 이상한 사진은 올리지 말아주세용 !
""",
)
async def get_inference_from_image(
    image: UploadFile, model_name: AiModel, threshold: float = 0.5
):
    url = upload_file_to_s3(image, "images")
    weight_file_path = f"ai/weights/{model_name.value}_qat.pt"
    return classify(
        url,
        weight_file_path=weight_file_path,
        model_name=model_name.value,
        threshold=threshold,
    )


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
