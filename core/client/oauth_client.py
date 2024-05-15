import json

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from fastapi import status, HTTPException
from google.auth import transport
from google.oauth2 import id_token
from jwt.algorithms import RSAAlgorithm

from core.config.var_config import IS_PROD
if IS_PROD:
    from core.config.var_config import APPLE_CLIENT_ID
else:
    from core.config.secrets import APPLE_CLIENT_ID
from core.dto.auth_dto import (
    GoogleCredentialsRequest,
    KakaoCredentialsRequest,
    AppleCredentialsRequest,
)


class OAuthClient:
    @classmethod
    def verify_google_token(cls, form: GoogleCredentialsRequest):
        try:
            user_info = id_token.verify_oauth2_token(
                id_token=form.id_token,
                audience=form.google_client_id,
                request=transport.requests.Request(),
            )
            return user_info
        except Exception as e:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Invalid Google credentials"
            )

    @classmethod
    def verify_kakao_token(cls, form: KakaoCredentialsRequest):
        response = requests.get(
            url='https://kapi.kakao.com/v2/user/me?property_keys=["kakao_account.email"]',
            headers={
                "Authorization": f"Bearer {form.access_token}",
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        if response.status_code != 200:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            finally:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, error_detail)

        return response.json()

    @classmethod
    def verify_apple_token(cls, form: AppleCredentialsRequest):
        id_token_header = jwt.get_unverified_header(form.id_token)
        jwks = requests.get("https://appleid.apple.com/auth/keys").json()["keys"]
        rsa_public_key = RSAAlgorithm.from_jwk(
            jwk=[
                json.dumps(jwk) for jwk in jwks if jwk["kid"] == id_token_header["kid"]
            ][0]
        ).public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        try:
            user_info = jwt.decode(
                jwt=form.id_token,
                key=rsa_public_key,
                algorithms=id_token_header["alg"],
                audience=APPLE_CLIENT_ID,
                options={"verify_signature": True},
            )
            return user_info
        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
