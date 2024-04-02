from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

from core.client.oauth_client import OAuthClient
from core.config.orm_config import transactional
from core.domain.user.user_model import User
from core.dto.auth_dto import AppleCredentialsRequest
from core.dto.auth_dto import GoogleCredentialsRequest
from core.dto.auth_dto import KakaoCredentialsRequest
from core.dto.auth_dto import TokenResponse
from core.util.jwt import build_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/sign-in/google",
    dependencies=[Depends(transactional)],
    response_model=TokenResponse,
)
async def sign_in_with_google(
    request: Request, google_credentials: GoogleCredentialsRequest
):
    user_info = OAuthClient.verify_google_token(google_credentials)

    user = User.get_or_none(
        User.uid == user_info["email"],
        User.is_deleted == False,
    )
    status_code = status.HTTP_200_OK
    if not user:
        status_code = status.HTTP_201_CREATED
        user = User.create(uid=user_info["email"], social_type="google")

    token = build_token(
        id=user.id,
        social_type=user.social_type,
        status=user.status,
    )

    response = JSONResponse(
        status_code=status_code,
        content=TokenResponse(user_id=user.id, access_token=token).model_dump(),
    )
    return response


@router.post(
    "/sign-in/kakao",
    dependencies=[Depends(transactional)],
    response_model=TokenResponse,
)
async def sign_in_with_kakao(
    request: Request, kakao_credentials: KakaoCredentialsRequest
):
    user_info = OAuthClient.verify_kakao_token(kakao_credentials)

    user = User.get_or_none(
        User.uid == user_info["kakao_account"]["email"], 
        User.is_deleted == False
    )
    status_code = status.HTTP_200_OK
    if not user:
        status_code = status.HTTP_201_CREATED
        user = User.create(
            uid=user_info["kakao_account"]["email"],
            social_type="kakao",
        )

    token = build_token(
        id=user.id,
        social_type=user.social_type,
        status=user.status,
    )
    return JSONResponse(
        status_code=status_code,
        content=TokenResponse(user_id=user.id, access_token=token).model_dump(),
    )


@router.post(
    "/sign-in/apple",
    dependencies=[Depends(transactional)],
    response_model=TokenResponse,
)
async def sign_in_with_apple(
    request: Request, apple_credentials: AppleCredentialsRequest
):
    user_info = OAuthClient.verify_apple_token(apple_credentials)

    user = User.get_or_none(
        User.social_type == "apple",
        User.uid == user_info["email"],
        User.is_deleted == False,
    )
    status_code = status.HTTP_200_OK
    if not user:
        status_code = status.HTTP_201_CREATED
        user = User.create(
            uid=user_info["email"],
            social_type="apple",
        )

    token = build_token(
        id=user.id,
        social_type=user.social_type,
        status=user.status,
    )

    return JSONResponse(
        status_code=status_code,
        content=TokenResponse(user_id=user.id, access_token=token).model_dump(),
    )
