from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

import requests
from google.oauth2 import id_token
from google.auth import transport

from src.orm import transactional
from v1.user.model import User
from v1.auth.model import GoogleCredentialsModel, KakaoCredentialsModel, AuthenticationResponse
from src.jwt import build_token
from src.config.var_config import JWT_COOKIE_OPTIONS


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/sign-in/google", dependencies=[Depends(transactional)], response_model=AuthenticationResponse)
async def sign_in_with_google(request: Request, google_credentials: GoogleCredentialsModel):
    form = google_credentials.model_dump()
    try:
        user_info = id_token.verify_oauth2_token(
            id_token=form["id_token"], 
            request=transport.requests.Request(), 
            audience=form["google_client_id"]
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"{e.__class__.__module__}.{e.__class__.__name__}", "message": str(e)}
        )
    
    user = User.get_or_none(
        User.social_type == "google",
        User.uid == user_info["email"],
        User.status == "active",
    )
    status_code = status.HTTP_200_OK
    if not user:
        status_code = status.HTTP_201_CREATED
        user = User.create(
            uid=user_info["email"],
            social_type="google",
        )

    token = build_token(
        id=user.id,
        social_type="google",
    )

    response = JSONResponse(
        status_code=status_code,
        content=AuthenticationResponse(access_token=token).model_dump()
    )
    response.set_cookie(value="token", **JWT_COOKIE_OPTIONS)
    return response


@router.post("/sign-in/kakao", response_model=AuthenticationResponse)
async def sign_in_with_kakao(request: Request, kakao_credentials: KakaoCredentialsModel):
    form = kakao_credentials.model_dump()
    oauth_response = requests.get(
        url='https://kapi.kakao.com/v2/user/me?property_keys=["kakao_account.email"]',
        # url="https://kapi.kakao.com/v1/user/access_token_info",
        headers={
            "Authorization": f"Bearer {form['access_token']}",
            # "Authorization": f"KakaoAK {KAKAO_ADMIN_KEY}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        },
    )
    if oauth_response.status_code != 200:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Kakao OAuth Error", "message": oauth_response.text}
        )

    user_info = oauth_response.json()
    status_code = status.HTTP_200_OK

    user = User.get_or_none(
        User.social_type == "kakao",
        User.uid == user_info["kakao_account"]["email"],
        User.status == "active",
    )
    if not user:
        status_code = status.HTTP_201_CREATED
        user = User.create(
            uid=user_info["kakao_account"]["email"],
            social_type="kakao",
        )
    
    token = build_token(
        id=user.id,
        social_type="kakao",
    )
    return JSONResponse(
        status_code=status_code,
        content=AuthenticationResponse(access_token=token).model_dump()
    )
