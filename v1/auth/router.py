from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

from google.oauth2 import id_token
from google.auth.transport import requests

from src.orm import transactional
from v1.auth.model import GoogleCredentialsModel
from v1.auth.jwt import build_token
from src.config.secrets import *
from src.config.var_config import JWT_COOKIE_OPTIONS


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/sign-in/google", dependencies=[])
async def sign_in_with_google(request: Request, google_credentials: GoogleCredentialsModel):
    form = google_credentials.model_dump()
    try:
        id_info = id_token.verify_oauth2_token(
            id_token=form["id_token"], 
            request=requests.Request(), 
            audience=form["google_client_id"]
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"{e.__class__.__module__}.{e.__class__.__name__}",
                "message": str(e),
            }
        )

    if form["nickname"] and form["preference"]: # 로그인
        # TODO get user from db
        token = build_token(

        )

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={}
        )

    else: # 회원가입
        # TODO add user to db
        token = build_token(

        )

        response = JSONResponse(
            status_code=status.HTTP_201_CREATED, 
            content={}
        )
    
    response.set_cookie(value="token", **JWT_COOKIE_OPTIONS)
    return response


@router.get("/sign-out")
async def sign_out(request: Request):
    response = JSONResponse(status_code=status.HTTP_200_OK, content={})
    response.delete_cookie(key="access_token")
    return response
