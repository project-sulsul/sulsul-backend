from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ai.inference import classify
from api.config.exceptions import ForbiddenException
from core.config.orm_config import transactional
from core.config.var_config import IS_PROD
from core.domain.user_model import User
from core.dto.auth_dto import TokenResponse
from core.util.jwt import build_token
from core.util.logger import logger

router = APIRouter(prefix="/test", tags=["테스트용 API"])


@router.get(
    "/jwt",
    dependencies=[Depends(transactional)],
    response_model=TokenResponse,
)
async def get_jwt_for_test(user_id: int):
    if IS_PROD:
        raise ForbiddenException(
            "This API is only available in development environment"
        )

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


@router.get("/ai")
async def get_inference_from_image(img_url: str):
    return classify(img_url)


@router.post("/error")
async def occur_unexpected_error(test_params: Optional[str] = None):
    raise Exception("Unexpected Error")
