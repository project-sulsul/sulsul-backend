from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

import jwt
import json
import requests
from jwt.algorithms import RSAAlgorithm
from cryptography.hazmat.primitives import serialization

from google.oauth2 import id_token
from google.auth import transport

from src.orm import transactional
from src.jwt import build_token
from v1.user.model import User
from v1.auth.model import GoogleCredentialsModel
from v1.auth.model import KakaoCredentialsModel
from v1.auth.model import AppleCredentialsModel
from v1.auth.model import TokenResponseModel


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/sign-in/google", dependencies=[Depends(transactional)], response_model=TokenResponseModel)
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
        User.is_deleted == False,
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
        content=TokenResponseModel(access_token=token).model_dump()
    )
    return response


@router.post("/sign-in/kakao", dependencies=[Depends(transactional)], response_model=TokenResponseModel)
async def sign_in_with_kakao(request: Request, kakao_credentials: KakaoCredentialsModel):
    form = kakao_credentials.model_dump()
    oauth_response = requests.get(
        url='https://kapi.kakao.com/v2/user/me?property_keys=["kakao_account.email"]',
        headers={
            "Authorization": f"Bearer {form['access_token']}",
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
        User.is_deleted == False
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
        content=TokenResponseModel(access_token=token).model_dump()
    )


@router.post("/sign-in/apple", dependencies=[Depends(transactional)], response_model=TokenResponseModel)
async def sign_in_with_apple(request: Request, apple_credentials: AppleCredentialsModel):
    form = apple_credentials.model_dump()

    id_token_header = jwt.get_unverified_header(form["id_token"])
    jwks = requests.get("https://appleid.apple.com/auth/keys").json()["keys"]
    rsa_public_key = RSAAlgorithm.from_jwk(
        jwk=[ json.dumps(jwk) for jwk in jwks if jwk["kid"] == id_token_header["kid"] ][0]
    ).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    user_info = jwt.decode(
        jwt=form["id_token"],
        key=rsa_public_key,
        algorithms=id_token_header["alg"],
        options={"verify_signature": True},
    )
    status_code = status.HTTP_200_OK

    user = User.get_or_none(
        User.social_type == "apple",
        User.uid == user_info["email"],
        User.is_deleted == False
    )

    return JSONResponse(status_code=status_code, content=TokenResponseModel(access_token=""))
