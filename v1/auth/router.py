from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from google.oauth2 import id_token
from google.auth.transport import requests

from .model import GoogleCredentialsModel
from .secrets import *
from .config import JWT_COOKIE_OPTIONS


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/sign-in/google")
async def sign_in_with_google(
    request: Request,
    google_credentials: GoogleCredentialsModel
):
    try:
        id_info = id_token.verify_oauth2_token(
            google_credentials.model_dump()["credential"], requests.Request(), 
            GOOGLE_CLIENT_ID,
        )
        
        # TODO add user to database
        # TODO generate JWT from Google ID Token

        response = JSONResponse(status_code=status.HTTP_200_OK, content={})
        response.set_cookie(value="token", **JWT_COOKIE_OPTIONS)
        return response

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": f"{e.__class__.__module__}.{e.__class__.__name__}",
                "error_type": "OAuth_Exception",
                "message": str(e),
            }
        )
    

@router.get("/sign-out")
async def sign_out(request: Request):
    response = JSONResponse(status_code=status.HTTP_200_OK, content={})
    response.delete_cookie(key="access_token")
    return response
